from __future__ import with_statement
import json

from fabric.api import local, prompt, task, settings, quiet
from fabric.colors import green, cyan
from fabric.contrib.console import confirm

from utils import get_commit_message, get_branch_name, post
from settings import GITHUB


@task(alias="ci")
def commit(message=None):
    with settings(warn_only=True):
        local('git status')
        prompt(cyan('Press <Enter> to continue or <Ctrl+C> to cancel.'))
        local('git add -A .')

        # Check if message present
        while not message:
            message = prompt(green("Enter commit message: "))

        # Default command
        command = 'git commit -a -u -m "%s"' % get_commit_message(message=message)

        local(command)


@task
def push(force=False):
    with settings(warn_only=True):
        command = 'git push origin %s' % get_branch_name()

        # Check if force commit is necessary
        if force:
            command += " --force"

        local(command)


@task(alias='pr')
def pull_request(message=None):

    title = get_commit_message(message=message)

    data = {
        "title": title,
        "body": "",
        "head": "{user}:{branch}".format(user=GITHUB['user'], branch=get_branch_name()),
        "base": "master"
    }

    response = post(url=GITHUB['urls']['pull_request'], data=json.dumps(data))

    print(cyan(response) if response.status_code != 201 else cyan("Pull request created."))


@task
def reset():
    local("git fetch upstream master")
    local("git reset --hard upstream/master")


@task
def change(number):
    with quiet():
        local("git branch task-%s" % number, capture=True)
    local("git checkout task-%s" % number)

    if confirm(cyan("Do you want to reset current branch?")):
        reset()


@task
def finish(message=None, force=False):
    commit(message=message)
    push(force=force)
    pull_request(message=message)
