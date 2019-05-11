# server.py
import subprocess as sp
import os


class Server(object):
    """docstring for Server"""
    def __init__(self, app_path, debug=False):
        super(Server, self).__init__()
        self.app_path = str(app_path)
        self.debug = bool(debug)
        self.set()

    def set(self):
        if self.debug:
            os.environ["FLASK_DEBUG"] = "1"
        else:
            os.environ["FLASK_DEBUG"] = "0"
        os.environ["FLASK_APP"] = self.app_path

    def start(self):
        sp.run("flask run", shell=True)

    def setDebug(self, arg):
        self.debug = bool(arg)

    def getDebug(self):
        return self.debug

    def setAppPath(self, app_path):
        self.app_path = str(app_path)

    def getAppPath(self):
        return self.app_path
