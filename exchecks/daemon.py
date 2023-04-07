import time
import sys
import os

from .configuration import DAEMONS
from .configuration import get_logger
from .cli import add_command
from .trackers import Tracker


class AlreadyRunningError(Exception):
    pass


def record_daemon(args):
    pid = os.getpid()
    PID_FILE = DAEMONS / f'{args.name}.pid'

    if PID_FILE.is_file():
        raise AlreadyRunningError(f'{PID_FILE} exists')

    with open(PID_FILE, 'w') as fh:
        fh.write(f'{pid}')

    logger, fh = get_logger(args.name, __name__)

    t = Tracker(pid)
    while PID_FILE.is_file():
        time.sleep(5)
        t.get_procs()
        t.report()


def daemon_exit(args):
    PID_FILE = DAEMONS / f'{args.name}.pid'
    if PID_FILE.is_file():
        PID_FILE.unlink()
    sys.exit(0)


def exit_parser_build(parser):
    parser.add_argument(
        "name",
        type=str,
        help="Daemon name",
    )
    parser.add_argument(
        "exit_code",
        type=int,
        help="Exit code of target command",
    )
    return parser


def record_parser_build(parser):
    parser.add_argument(
        "name",
        type=str,
        help="Daemon name",
    )
    return parser


add_command(
    name='record',
    function=record_daemon,
    parser_build=record_parser_build,
    command_help='Record child processes',
)

add_command(
    name='exit',
    function=daemon_exit,
    parser_build=exit_parser_build,
    command_help='Stop record and report last exit code',
)
