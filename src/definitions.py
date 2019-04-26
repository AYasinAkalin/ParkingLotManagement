# definitions.py
'''
Contains project wide(global) variables
'''
from pathlib import Path
import os


def init():
    '''
    Creates project wide global variables to be reached within other files
    '''
    # DIR_SRC points to folder of source codes which is *PROJECT_DIRECTORY*/src
    # and can be reached from definitions.DIR_SRC after
    # running definitions.init() just once
    global DIR_SRC
    DIR_SRC = Path(__file__).parent

    if Path.cwd() is not DIR_SRC:
        # Changes active directory to project directory
        os.chdir(DIR_SRC)

    global FILE_REQS
    FILE_REQS = DIR_SRC.resolve().parent / "requirements.txt"

    global DEBUG
    DEBUG = True
