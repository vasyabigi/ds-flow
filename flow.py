"""Workflow helper.

Usage:
  flow <command>

List of availible commands:
   commit       Add file contents to the index


"""
import tasks


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__, version='Workflow helper 0.0.1')
    print(arguments)

    # TODO:
    command = arguments.get("<command>")
    getattr(tasks, command)()
