import pathlib
import configparser
import os
import logging


def setup_logging(args):
    level = logging.DEBUG if args.verbose else logging.INFO

    if args.persist:
        logfile = get_logfile(args.name)
        fh = logging.FileHandler(logfile, 'w')
        fh.setLevel(level)

    for name, item in logging.root.manager.loggerDict.items():
        if isinstance(item, logging.Logger):
            item.setLevel(level)
            if args.persist:
                item.addHandler(fh)


def get_datafile(name):
    return CHECKS / f'{name}.data'


def get_logfile(fname):
    return CONF_FOLDER / f'{fname}.log'


config = configparser.ConfigParser()

HOME = pathlib.Path(os.path.expanduser("~"))
CONF_FOLDER = HOME / '.config' / 'exchecks'
CONF_FILE = CONF_FOLDER / 'config'
CHECKS = CONF_FOLDER / 'checks'
DAEMONS = CONF_FOLDER / 'daemons'

if not CONF_FOLDER.is_dir():
    CONF_FOLDER.mkdir(parents=True)

if not DAEMONS.is_dir():
    DAEMONS.mkdir(parents=True)

if not CHECKS.is_dir():
    CHECKS.mkdir(parents=True)

DEFAULT = {
    'Checkers': {
        'check-interval': 10.0,
    },
    'Client': {
        'address': '127.0.0.1',
        'port': 8888,
    },
    'Server': {
    }
}

config.read_dict(DEFAULT)

if CONF_FILE.exists():
    config.read([CONF_FILE])
