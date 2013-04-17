"""
Usage:
    flow <command> [options]

Options:
    -m MESSAGE      Command message
    -f              Force
    -t NUMBER       Task number

List of availible commands:
   commit           Add file contents to the index
   push             Update remote refs along with associated objects
   pull_request     Send pull request to github
   change           Go to other branch. Start working on new task
   finish           Finish current task
   reset            Reset current branch. Update with last upstream changes


"""
import os
from utils import ALIAS
from fabric.api import local


PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))


def get_fab_args(arguments):
    args = []
    for key, value in arguments.iteritems():
        if value:
            value = "'%s'" % value if isinstance(value, str) else value
            args.append("%s=%s" % (ALIAS.get(key, key), value))

    return ",".join(args)


def run_command(arguments):
    command_name = arguments.pop('<command>')

    command = "fab -f %s/tasks.py %s" % (PROJECT_PATH, command_name)

    additional_args = get_fab_args(arguments)
    if additional_args:
        command += ":%s" % additional_args

    local(command)


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__, version='Workflow helper 0.0.1')
    run_command(arguments)
