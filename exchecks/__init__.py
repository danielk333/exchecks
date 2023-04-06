#This is needed so that the registration is performed
from . import website

#Then expose the main after registration
from .cli import main
