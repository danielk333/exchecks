import argparse

from .configuration import config
from .configuration import DATA_FILE

COMMANDS = dict()


def add_command(name, function, parser_build, command_help=''):
    global COMMANDS
    COMMANDS[name] = dict()
    COMMANDS[name]['function'] = function
    COMMANDS[name]['parser'] = (parser_build, command_help)


def main():
    parser = argparse.ArgumentParser(description='Python package to track long running executions')
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', action='count', default=0)

    subparsers = parser.add_subparsers(help='Avalible command line interfaces', dest='command')
    subparsers.required = True

    for name, dat in COMMANDS.items():
        parser_builder, command_help = dat['parser']
        cmd_parser = subparsers.add_parser(name, help=command_help)
        parser_builder(cmd_parser)

    args = parser.parse_args()

    function = COMMANDS[args.command]['function']
    function(args)
