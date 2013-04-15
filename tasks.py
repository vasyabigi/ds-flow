from __future__ import with_statement
from fabric.api import local

from utils import memoize


@memoize
def get_branch_name():
    branch = local("git rev-parse --abbrev-ref HEAD", capture=True)
    return branch


def commit():
    branch_name = get_branch_name()
    return branch_name
