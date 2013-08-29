GITHUB_USER = ''
GITHUB_PASS = ''
GITHUB_PULL_REQUEST_URL = 'https://api.github.com/repos/django-stars/mmp/pulls'

TASK_PREFIX = "task-"

UPSTREAM_ONLY = False

GIT_ADD_FIRST = False
GIT_REBASE_FIRST = False
GIT_REMOTE_NAME = "upstream"

from local_settings import *

GITHUB = {
    'user': GITHUB_USER,
    'password': GITHUB_PASS,
    'urls': {
        'pull_request': GITHUB_PULL_REQUEST_URL
    }
}
