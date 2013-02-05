# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import json
from functools import partial

from requests import get, post

from fabric.api import cd, local

RUN_DIR = os.getcwd()
GITHUB = {
    'user': '',
    'password': '',
    'urls': {
        'base': 'https://api.github.com',
        'pull_request': '/repos/django-stars/mmp/pulls'
    }
}


get = partial(get, auth=(GITHUB['user'], GITHUB['password']))
post = partial(post, auth=(GITHUB['user'], GITHUB['password']))


def git_checkout(where):
    local("git checkout %s" % where)


def git_reset(branch="upstream/master"):
    local("git reset --hard %s" % branch)


def git_fetch(remote="upstream"):
    local("git fetch %s" % remote)


def git_new_branch(name):
    local("git branch %s" % name)


def git_rebase(branch="upstream/master"):
    local("git rebase -i %s" % branch)


def git_get_branch_name():
    result = local("git branch", capture=True)
    branch_name = None
    for bn in result.split("\n"):
        if bn.startswith("*"):
            branch_name = bn.split()[-1]
            break

    assert branch_name, "No branch name captured"

    return branch_name


def git_push(where, force=False):
    command = ["git push origin %s" % where]
    if force:
        command.append("-f")
    local(" ".join(command))


def git_collect_commits_messages(start="upstream/master", end=None):
    if not end:
        end = git_get_branch_name()
    command = 'git log --pretty=format:"%s" {start}..{end}'.format(
        start=start,
        end=end
    )
    result = local(
        command,
        capture=True
    )

    filter_task_name = lambda i: i.split(", ")[-1]

    result = ". ".join(map(filter_task_name, result.split("\n")))
    return result


def git_pull_request():
    branch_name = git_get_branch_name()
    pull_request_title = (
        raw_input("Pull request title: ")
        or git_collect_commits_messages()
    )
    pull_request_title = ", ".join([branch_name.capitalize(), pull_request_title])
    data = {
        "title": pull_request_title,
        "body": "",
        "head": "{user}:{branch}".format(
            user=GITHUB['user'], branch=branch_name
        ),
        "base": "master"
    }
    url = "".join([GITHUB['urls']['base'], GITHUB['urls']['pull_request']])
    response = post(url=url, data=json.dumps(data))
    assert response.status_code == 201


def migrate(app_name=None):
    command = ["python manage.py migrate"]
    if app_name:
        command.append(app_name)
    local(" ".join(command))


def test(app_name=None):
    command = ["python manage.py test --settings=settings_test"]
    if app_name:
        command.append(app_name)
    command.append("; alert 'finished'")
    local(" ".join(command))


def new_task(task_number):
    assert task_number, "No task number given"

    branch_name = "task-%s" % task_number

    with cd(RUN_DIR):
        git_checkout("master")
        git_fetch()
        git_reset()
        git_new_branch(branch_name)
        git_checkout(branch_name)
        migrate()


def update_task():
    """Should be runned after checkout"""

    git_fetch()
    git_rebase()
    migrate()


def reopen_task(task_number):
    assert task_number, "No task number given"

    branch_name = "task-%s" % task_number

    with cd(RUN_DIR):
        git_checkout(branch_name)
        update_task()


def switch_to_task(task_number, update=True):
    assert task_number, "No task number given"

    branch_name = "task-%s" % task_number
    with cd(RUN_DIR):
        git_checkout(branch_name)
        update_task()


def finish_task():
    with cd(RUN_DIR):
        # test()
        git_fetch()
        git_rebase()

        branch_name = git_get_branch_name()

        git_push(branch_name)
        git_pull_request()
