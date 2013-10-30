import os
from ConfigParser import ConfigParser


class FlowHandler(object):
    def __init__(self, conf_filename=".flow"):
        self.conf_filename = conf_filename

    def get_filenames(self, path):
        path_list = []

        while True:
            path_list.insert(0, os.path.join(path, self.conf_filename))
            newpath = os.path.dirname(path)
            if path == newpath:
                break
            path = newpath

        if not len(path_list):
            raise Exception('Please, create %s config file with required credentials' % self.conf_filename)

        return path_list

    def get_configurations(self):
        conf_files = self.get_filenames(os.getcwd())
        parser = ConfigParser()

        # Defaults:
        parser.add_section('global')
        parser.set('global', 'UPSTREAM_ONLY', False)
        parser.set('global', 'GIT_ADD_FIRST', False)
        parser.set('global', 'GIT_REBASE_FIRST', False)
        parser.set('global', 'GIT_REMOTE_NAME', 'upstream')
        parser.set('global', 'GIT_DEFAULT_BASE', 'master')
        parser.set('global', 'GITHUB_PULL_REQUEST_URL', 'https://api.github.com/repos/django-stars/mmp/pulls')

        parser.read(conf_files)

        return parser

parser = FlowHandler()
config = parser.get_configurations()

GITHUB_USER = config.get('global', 'GITHUB_USER')
GITHUB_PASS = config.get('global', 'GITHUB_PASS')
GIT_ADD_FIRST = config.getboolean('global', 'GIT_ADD_FIRST')
GIT_REBASE_FIRST = config.getboolean('global', 'GIT_REBASE_FIRST')
GIT_REMOTE_NAME = config.get('global', 'GIT_REMOTE_NAME')
UPSTREAM_ONLY = config.getboolean('global', 'UPSTREAM_ONLY')
GITHUB_PULL_REQUEST_URL = config.get('global', 'GITHUB_PULL_REQUEST_URL')
GIT_DEFAULT_BASE = config.get('global', 'GIT_DEFAULT_BASE')
