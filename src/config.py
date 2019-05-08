import definitions
definitions.init()

# ########################
# DIRECTORIES
# ########################
''' Define new directory variables according to following rules:
    1) Use CAPITAL LETTERS
    2) Start with phrase 'DIR'
    3) Use '_' as delimiter
'''
DIR_SRC = definitions.DIR_SRC  # Points to the folder source code is being held
DIR_ROOT = DIR_SRC.parent  # Points to Root directory of the project

# ########################
# SINGLE FILES
# ########################
''' Define new file variables according to following rules:
    1) Use CAPITAL LETTERS
    2) Start with phrase 'FILE'
    3) Use '_' as delimiter
'''
FILE_REQS = definitions.FILE_REQS  # Points to requirements.txt

# ########################
# SETTINGS
# ########################
DEMO = False
VERBOSE = False
DEBUG = False
CLEAN_DB = True
