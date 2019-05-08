# __main__.py
import subprocess as sp
import database
import config
cmd = 'pip install -r ' + str(config.FILE_REQS)
sp.run(cmd, shell=True)
database.init("parkinglot.db", clean=config.CLEAN_DB)
if config.DEBUG:
    sp.run('export FLASK_DEBUG=1', shell=True)
sp.run('export FLASK_APP=app.py', shell=True)
sp.run('flask run', shell=True)
