from __future__ import with_statement

import json

from fabric.api import local, prompt, task, quiet
from fabric.colors import green, cyan, red
from fabric.contrib.console import confirm

from settings import GITHUB, UPSTREAM_ONLY, TASK_PREFIX, GIT_REMOTE_NAME, GIT_DEFAULT_BASE
from utils import get_commit_message, get_branch_name, post


@task(alias="ci")
def commit(message=None, amend=False, add_first=False):
    git_status = local('git status --short', capture=True)

    if not git_status:
        print(cyan('Nothing to commit.'))
        return

    if add_first:
        local("git add .")

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

    if not local("git diff --cached", capture=True):
        print(red("Your commit is empty. Please add something and try again."))
    else:
        local(command)

        if amend:
            print(cyan("Commited with amend."))
        else:
            print(cyan("Commited with message: " + get_commit_message(message=message)))


@task
def push(force=False, need_rebase=False, base=GIT_DEFAULT_BASE):
    if need_rebase:
        rebase()

    print(cyan("Pushing..."))

    if UPSTREAM_ONLY:
        command = 'git push %s %s:%s' % (GIT_REMOTE_NAME, get_branch_name(), base)
    else:
        command = 'git push origin %s' % get_branch_name()

    # Check if force commit is necessary
    if force:
        command += " --force"

    local(command)

    print(cyan("Pushed."))


@task(alias='pr')
def pull_request(message=None, base=GIT_DEFAULT_BASE):
    print(cyan("Sending pull request..."))

    if confirm(green('Default message: %s' % get_commit_message(message=message))):
        title = get_commit_message(message=message)
    else:
        title = get_commit_message(message=prompt(green("Enter message: ")))

    data = {
        "title": title,
        "body": "",
        "head": "{user}:{branch}".format(user=GITHUB['user'], branch=get_branch_name()),
        "base": base
    }

    response = post(url=GITHUB['urls']['pull_request'], data=json.dumps(data))

    print(cyan(response) if response.status_code != 201 else cyan("Pull Request was sent."))


@task
def reset(base=GIT_DEFAULT_BASE):
    local("git fetch %s" % GIT_REMOTE_NAME)
    local("git reset --hard %s/%s" % (GIT_REMOTE_NAME, base))


@task
def rebase(base=GIT_DEFAULT_BASE):
    print(cyan("Rebasing..."))
    local("git fetch %s" % GIT_REMOTE_NAME)
    local("git rebase %s/%s" % (GIT_REMOTE_NAME, base))
    print(cyan("Rebase finished."))


@task
def change(number, prefix=TASK_PREFIX, base=GIT_DEFAULT_BASE):
    with quiet():
        local("git branch %s%s" % (prefix, number))
        local("git checkout %s%s" % (prefix, number))
        print(cyan("Changed to %s." % get_branch_name()))

    if confirm(green("Do you want to reset current branch?")):
        reset(base=base)
        print(cyan("Got last changes from %s." % GIT_REMOTE_NAME))


@task
def finish(message=None, force=False, need_rebase=False, add_first=False, base=GIT_DEFAULT_BASE):
    commit(message=message, add_first=add_first)

    push(force=force, need_rebase=False, base=base)

    if not UPSTREAM_ONLY:
        pull_request(message=message, base=base)


@task
def fix(base=GIT_DEFAULT_BASE):
    change(number="quick-fix", prefix="", base=base)
