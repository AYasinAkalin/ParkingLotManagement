# __main__.py
import subprocess as sp
import definitions
import database
definitions.init()
cmd =  'pip install -r requirements.txt'# + str(definitions.FILE_REQS)
sp.run(cmd, shell=True)
database.init("parkinglot.db")
if definitions.DEBUG:
    sp.run('export FLASK_DEBUG=1', shell=True)
sp.run('export FLASK_APP=app.py', shell=True)
sp.run('flask run', shell=True)
