from __future__ import with_statement

import json

from fabric.api import local, prompt, task, quiet
from fabric.colors import green, cyan
from fabric.contrib.console import confirm

from settings import GITHUB
from utils import get_commit_message, get_branch_name, post


@task(alias="ci")
def commit(message=None, amend=False):
    print(cyan('Review git status:'))
    local('git status')
    prompt(cyan('Press <Enter> to continue or <Ctrl+C> to cancel.'))

    # Default command
    command = 'git commit'

    if amend:
        command += " --amend"
    else:
        # Check if message present
        while not message:
            message = prompt(green("Enter commit message: "))

        command += ' -a -u -m "%s"' % get_commit_message(message=message)

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

    title = prompt(
        'Enter pull request title or use default on <Enter>:',
        default=get_commit_message(message=message)
    )

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
    local("git fetch upstream master")
    local("git reset --hard upstream/master")


@task
def change(number):
    with quiet():
        local("git branch task-%s" % number)
        local("git checkout task-%s" % number)
        print(cyan("Already on %s" % get_branch_name()))

    if confirm(cyan("Do you want to reset current branch?")):
        reset()
        print(cyan("Got last changes from upstream."))


@task
def finish(message=None, force=False):
    commit(message=message)
    push(force=force)
    pull_request(message=message)