# __main__.py
import subprocess as sp
import definitions
definitions.init()
if definitions.DEBUG:
    sp.run('export FLASK_DEBUG=1', shell=True)
sp.run('export FLASK_APP=hello.py', shell=True)
sp.run('flask run', shell=True)
