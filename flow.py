"""Workflow helper.

Usage:
    flow [options] <command>

Options:
    -f              Force
    -m MESSAGE      Command message

List of availible commands:
   commit       Add file contents to the index
   push         Update remote refs along with associated objects
   finish       Finish current task


"""
import tasks


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__, version='Workflow helper 0.0.1')
    tasks.run_command(arguments)
