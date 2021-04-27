import configparser, os, shutil

from ..utils.funcs import path_desktop

class ConfigParser(configparser.ConfigParser):
    def get(self, section, option, default=None, *args, **kwargs):
        try:
            return super().get(section, option, *args, **kwargs)
        except configparser.NoOptionError:
            return default

    def getint(self, section, option, default=None, *args, **kwargs):
        try:
            return super().getint(section, option, *args, **kwargs)
        except configparser.NoOptionError:
            return default

configset = {
    'defaultareamode': (str, 'Quadrangle'),
    'defaultpredmode': (str, 'image'),

    'lastOpenDir': (str, path_desktop()),
    'credentialJsonpath': (str, None),

    'export_defaultFileFormat': (str, 'CSV'),
    'export_sameRowY': (int, 10),
    'export_sameColX': (int, 15),

    'export_datasetFormat': (str, 'VOC'),
    'export_datasetDir': (str, None)
}

class Config(object):
    selectedImgDir = os.path.join('.tda', 'selectedImg')
    tmpDir = os.path.join('.tda', 'tmp')
    iniPath = os.path.join('.tda', 'tda.ini')

    defaultareamode: str

    def __init__(self):
        self.config = ConfigParser(allow_no_value=True)

        self._initialReadConfig()

    @property
    def configpath(self):
        return self.iniPath

    def __getattr__(self, attr):
        if attr in configset.keys():
            cls, default = configset[attr]
            if cls is str:
                return self.config.get('settings', attr, default)
            elif cls is int:
                return self.config.getint('settings', attr, default)
            else:
                assert False, "Bug was occurred"

    def __setattr__(self, attr, value):
        if attr in configset.keys():
            self.config.set('settings', attr, str(value))
            self.writeConfig()
        else:
            super().__setattr__(attr, value)


    def _initialReadConfig(self):
        # create .tda directory
        if not os.path.exists('.tda'):
            os.makedirs('.tda')

        # create config file if not exist
        if not os.path.exists(self.configpath):
            # initial creation
            if os.path.exists('.tda'):
                shutil.rmtree('.tda') # remove all
                os.makedirs('.tda')

            # set default value
            self.config['default'] = configset
            self.config['settings'] = configset

            # write
            self.writeConfig()

        if not os.path.exists(self.selectedImgDir):
            os.makedirs(self.selectedImgDir)
        if not os.path.exists(self.tmpDir):
            os.makedirs(self.tmpDir)

        # read
        self.readConfig()

    def readConfig(self):
        self.config.read(self.configpath)

    def writeConfig(self):
        with open(self.configpath, 'w') as f:
            self.config.write(f)