# This is needed so that the registration is performed
from . import website
from . import daemon

# Then expose the main after registration
from .cli import main
