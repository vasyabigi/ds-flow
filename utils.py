from functools import wraps
from fabric.api import local, quiet

ALIAS = {
    '-f': 'force',
    '-m': 'message'
}


def memoize(func):

    cache = {}

    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap


@memoize
def get_branch_name():
    with quiet():
        branch = local("git rev-parse --abbrev-ref HEAD", capture=True)
    return branch


def get_commit_message(message):
    branch_name = get_branch_name()
    return "%s, %s" % (branch_name.capitalize(), message)
