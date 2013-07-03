import os, ConfigParser

user_dir = os.path.expanduser('~')
config_file = os.path.join(user_dir, '.flow')


class ConfigurationException(Exception):
    pass

def get_config_files():
    env_config_file = os.environ.get('FLOW_CONFIG_FILE', False)
    if env_config_file:
        return [env_config_file]
    if os.path.exists(config_file):
        return [config_file]
    else:
        raise ConfigurationException('Please, create ~/.flow config file with required credentials')

config = ConfigParser.ConfigParser()
config.read(get_config_files())

GITHUB_USER = config.get('global', 'GITHUB_USER')
GITHUB_PASS = config.get('global', 'GITHUB_PASS')

UPSTREAM_ONLY = config.getboolean('global', 'UPSTREAM_ONLY')
