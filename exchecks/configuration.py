import pathlib
import configparser
import os
import logging


def get_logger(fname, name, level=logging.DEBUG):

    logfile = CONF_FOLDER / f'{fname}.log'

    logger = logging.getLogger(name)

    logger.setLevel(level)
    logger.propagate = False

    fh = logging.FileHandler(logfile, 'w')
    fh.setLevel(level)
    logger.addHandler(fh)

    return logger, fh


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
    'General': {
    },
}

config.read_dict(DEFAULT)

if CONF_FILE.exists():
    config.read([CONF_FILE])
else:
    with open(CONF_FILE, 'w') as configfile:
        config.write(configfile)
