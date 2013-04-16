from __future__ import with_statement
from fabric.api import local, prompt, task, settings
from fabric.colors import green

from utils import get_commit_message, get_branch_name

try:
    from local_settings import *
except ImportError:
    pass


@task(alias="ci")
def commit(message=None):
    with settings(warn_only=True):
        local('git status')
        prompt(green('Press <Enter> to continue or <Ctrl+C> to cancel.'))
        local('git add -A .')

        # Check if message present
        while not message:
            message = prompt(green("Enter commit message: "))

        # Default command
        command = 'git commit -a -u -m "%s"' % get_commit_message(message)

        local(command)


@task
def push(force=False):
    with settings(warn_only=True):
        command = 'git push origin %s' % get_branch_name()

        # Check if force commit is necessary
        if force:
            command + " --force"

        local(command)


@task(alias="pr")
def pull_request(message=None):
    pass


def reset():
    local("git fetch upstream/master")
    local("git reset --hard upstream/master")


@task
def finish(message=None, force=False):
    commit(message=message)
    push(force=force)
    # pull_request(message=message)
