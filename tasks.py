from __future__ import with_statement

import json

from fabric.api import local, prompt, task, quiet
from fabric.colors import green, cyan
from fabric.contrib.console import confirm

from settings import GITHUB
from utils import get_commit_message, get_branch_name, post


@task(alias="ci")
def commit(message=None, amend=False):
    git_status = local('git status --short', capture=True)

    if not git_status:
        print(cyan('Nothing to commit.'))
        return

    print(cyan('Review git status:'))

    local('git status --short')
    prompt(cyan('Press <Enter> to continue or <Ctrl+C> to cancel.'))

    # Default command
    command = 'git commit'

    if amend:
        command += " --amend"
    else:
        # Check if message present
        while not message:
            message = prompt(green("Enter commit message: "))

        command += ' -m "%s"' % get_commit_message(message=message)

    local(command)

    if amend:
        print(cyan("Commited with amend."))
    else:
        print(cyan("Commited with message: " + get_commit_message(message=message)))


@task
def push(force=False):
    print(cyan("Pushing..."))

    command = 'git push origin %s' % get_branch_name()

    # Check if force commit is necessary
    if force:
        command += " --force"

    local(command)

    print(cyan("Pushed."))


@task(alias='pr')
def pull_request(message=None):
    print(cyan("Sending pull request..."))

    if confirm(green('Default message: %s' % get_commit_message(message=message))):
        title = get_commit_message(message=message)
    else:
        title = get_commit_message(message=prompt(green("Enter message: ")))

    data = {
        "title": title,
        "body": "",
        "head": "{user}:{branch}".format(user=GITHUB['user'], branch=get_branch_name()),
        "base": "master"
    }

    response = post(url=GITHUB['urls']['pull_request'], data=json.dumps(data))

    print(cyan(response) if response.status_code != 201 else cyan("Pull Request was sent."))


@task
def reset():
    local("git fetch upstream")
    local("git reset --hard upstream/master")


@task
def rebase():
    local("git fetch upstream")
    local("git rebase upstream/master")


@task
def change(number, prefix="task-"):
    with quiet():
        local("git branch %s%s" % (prefix, number))
        local("git checkout %s%s" % (prefix, number))
        print(cyan("Changed to %s." % get_branch_name()))

    if confirm(green("Do you want to reset current branch?")):
        reset()
        print(cyan("Got last changes from upstream."))


@task
def finish(message=None, force=False):
    commit(message=message)
    push(force=force)
    pull_request(message=message)


@task
def fix():
    change(number="quick-fix", prefix="")
