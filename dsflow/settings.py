GITHUB_USER = ''
GITHUB_PASS = ''

GITHUB = {
    'user': GITHUB_USER,
    'password': GITHUB_PASS,
    'urls': {
        'pull_request': 'https://api.github.com/repos/django-stars/mmp/pulls'
    }
}

TASK_PREFIX = "task-"

UPSTREAM_ONLY = False

GIT_ADD_FIRST = False
GIT_REBASE_FIRST = False

from local_settings import *
