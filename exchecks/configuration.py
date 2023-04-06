import pathlib
import configparser
import os

config = configparser.ConfigParser()

HOME = pathlib.Path(os.path.expanduser("~"))
CONF_FOLDER = HOME / '.config' / 'exchecks'
CONF_FILE = CONF_FOLDER / 'config'
DATA_FILE = CONF_FOLDER / 'checks.json'

if not CONF_FOLDER.is_dir():
    CONF_FOLDER.mkdir(parents=True)

DEFAULT = {
    'General': {
    },
}

config.read_dict(DEFAULT)

if not DATA_FILE.exists():
    DATA_FILE.touch()

if CONF_FILE.exists():
    config.read([CONF_FILE])
else:
    with open(CONF_FILE, 'w') as configfile:
        config.write(configfile)
