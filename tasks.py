from __future__ import with_statement
from fabric.api import local, prompt, task

from utils import ALIAS, get_commit_message, get_branch_name


@task(alias="ci")
def commit(message=None):

    # Check if message present
    while not message:
        message = prompt("Enter commit message:")

    # Default command
    command = 'git commit -m "%s"' % get_commit_message(message)

    local(command)


@task
def push(force=False):
    command = 'git push origin %s' % get_branch_name()

    # Check if force commit is necessary
    if force:
        command + " --force"

    local(command)


@task(alias="pr")
def pull_request(message=None):
    pass


@task
def finish(message=None, force=False):
    commit(message=message)
    push(force=force)
    # pull_request(message=message)


def get_fab_args(arguments):
    args = []
    for key, value in arguments.iteritems():
        if value:
            value = "'%s'" % value if isinstance(value, str) else value
            args.append("%s=%s" % (ALIAS.get(key, key), value))

    return ",".join(args)


def run_command(arguments):
    command_name = arguments.pop('<command>')

    command = "fab -f tasks.py %s" % command_name

    additional_args = get_fab_args(arguments)
    if additional_args:
        command += ":%s" % additional_args

    local(command)
