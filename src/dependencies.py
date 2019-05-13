# dependencies.py
import config
import subprocess as sp


class Dependency(object):
    """A simple class to install dependencies listed in requirements.txt
    Call install_all() function to install dependencies automatically.
    """

    def __init__(self):
        self.options = ''
        self.options_flag = False

    def __set_options(self):
        ''' Set parameters to attach to `pip install` cmd. using config.py'''
        if self.options_flag is False:
            try:
                if config.SILENT_INSTALL:
                    self.options += ' --quiet'
            except Exception as e:
                print(e)
        self.options_flag = True

    def install_all(self):
        ''' Install all dependencies listed in requirements.txt '''
        self.__set_options()
        cmd = 'pip install' + self.options + ' -r ' + str(config.FILE_REQS)
        sp.run(cmd, shell=True)
