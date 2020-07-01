import configparser, os, shutil

from .utils import path_desktop

class Config(object):
    def __init__(self):
        self.config = configparser.ConfigParser()

        self._initialReadConfig()

    @property
    def configpath(self):
        return os.path.join('.mda', 'mda.ini')

    @property
    def last_opendir(self):
        return self.config['settings']['last_opendir']
    @last_opendir.setter
    def last_opendir(self, last_dir):
        self.config['settings']['last_opendir'] = last_dir
        self.writeConfig()

    def _initialReadConfig(self):
        if not os.path.exists(self.configpath):
            # initial creation
            if os.path.exists('.mda'):
                shutil.rmtree('.mda') # remove all
            os.makedirs('.mda')

            # default value
            default = {
                'last_opendir': path_desktop()

            }

            self.config['default'] = default
            self.config['settings'] = default

            # write
            self.writeConfig()

        # read
        self.readConfig()

    def readConfig(self):
        self.config.read(self.configpath)

    def writeConfig(self):
        with open(self.configpath, 'w') as f:
            self.config.write(f)