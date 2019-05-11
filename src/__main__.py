# __main__.py
import subprocess as sp
import definitions
import database
import server
import config
definitions.init()

# Install dependencies
options = ''
if config.SILENT_INSTALL:
    options += ' --quiet'
cmd = 'pip install' + options + ' -r ' + str(config.FILE_REQS)
sp.run(cmd, shell=True)

# Set the database
database.init(config.FILE_DATABASE)
sp.run('export FLASK_APP=app.py', shell=True)
sp.run('flask run', shell=True)
