import configparser, os, shutil

from .utils import path_desktop

class Config(object):
    def __init__(self):
        self.config = configparser.ConfigParser()

        self._initialReadConfig()

    @property
    def configpath(self):
        return os.path.join('.tda', 'tda.ini')

    @property
    def last_opendir(self):
        return self.config['settings']['lastOpenDir']
    @last_opendir.setter
    def last_opendir(self, last_dir):
        self.config['settings']['lastOpenDir'] = last_dir
        self.writeConfig()

    @property
    def credentialJsonpath(self):
        if self.config['settings']['credentialJsonpath'] == 'None':
            return None
        return self.config['settings']['credentialJsonpath']
    @credentialJsonpath.setter
    def credentialJsonpath(self, path):
        self.config['settings']['credentialJsonpath'] = path
        self.writeConfig()

    def _initialReadConfig(self):
        if not os.path.exists(self.configpath):
            # initial creation
            if os.path.exists('.tda'):
                shutil.rmtree('.tda') # remove all
            os.makedirs('.tda')
            os.makedirs(os.path.join('.tda', 'tmp'))

            # default value
            default = {
                'lastOpenDir': path_desktop(),
                'credentialJsonpath': 'None'
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