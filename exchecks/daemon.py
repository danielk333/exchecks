import time
import sys
import os
import logging

from .configuration import DAEMONS
from .configuration import setup_logging, get_datafile
from .configuration import config
from .cli import add_command
from .trackers import Tracker

logger = logging.getLogger(__name__)


class AlreadyRunningError(Exception):
    pass


def get_pid_file(args):
    return DAEMONS / f'{args.name}.pid'


def record_daemon(args):
    pid = os.getpid()
    PID_FILE = get_pid_file(args)

    setup_logging(args)

    if PID_FILE.is_file():
        raise AlreadyRunningError(f'{PID_FILE} exists')

    with open(PID_FILE, 'w') as fh:
        fh.write(f'{pid}')

    dt = config.getfloat('Checkers', 'check-interval')

    data_file = get_datafile(args.name)
    if data_file.is_file():
        data_file.unlink()

    t = Tracker(pid, args.name)
    while PID_FILE.is_file():
        t.get_procs()
        t.report()
        time.sleep(dt)

    t.finish()
    if not args.persist:
        data_file = get_datafile(args.name)
        data_file.unlink()


def daemon_exit(args):
    PID_FILE = get_pid_file(args)
    if PID_FILE.is_file():
        with open(PID_FILE, 'r') as fh:
            pid = int(fh.read())

        t = Tracker(pid, args.name)
        t.finish(args.exit_code)

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
        help="Exit code to report",
    )
    return parser


def record_parser_build(parser):
    parser.add_argument(
        "name",
        type=str,
        help="Daemon name",
    )
    parser.add_argument(
        '-p', '--persist', 
        action='store_true',
        help='Persist checks data'
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
