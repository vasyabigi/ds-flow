from local_settings import GITHUB_USER, GITHUB_PASS

GITHUB = {
    'user': GITHUB_USER,
    'password': GITHUB_PASS,
    'urls': {
        'pull_request': 'https://api.github.com/repos/django-stars/mmp/pulls'
    }
}

UPSTREAM_PUSH = False
