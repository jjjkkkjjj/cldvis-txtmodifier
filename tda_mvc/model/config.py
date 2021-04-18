import configparser, os, shutil

from ..utils.funcs import path_desktop

class Config(object):
    selectedImgDir = os.path.join('.tda', 'selectedImg')
    iniPath = os.path.join('.tda', 'tda.ini')

    def __init__(self):
        self.config = configparser.ConfigParser(allow_no_value=True)

        self._initialReadConfig()

    @property
    def configpath(self):
        return self.iniPath

    @property
    def lastOpenDir(self):
        return self.config.get('settings', 'lastOpenDir')
    @lastOpenDir.setter
    def lastOpenDir(self, last_dir):
        self.config.set('settings', 'lastOpenDir', last_dir)
        self.writeConfig()

    @property
    def credentialJsonpath(self):
        return self.config.get('settings', 'credentialJsonpath')
    @credentialJsonpath.setter
    def credentialJsonpath(self, path):
        self.config.set('settings', 'credentialJsonpath', path)
        self.writeConfig()

    @property
    def export_defaultFileFormat(self):
        return self.config.get('settings', 'export_defaultFileFormat')
    @export_defaultFileFormat.setter
    def export_defaultFileFormat(self, value):
        self.config.set('settings', 'export_defaultFileFormat', value)
        self.writeConfig()

    @property
    def export_sameRowY(self):
        return self.config.getint('settings', 'export_sameRowY')
    @export_sameRowY.setter
    def export_sameRowY(self, value):
        self.config.set('settings', 'export_sameRowY', str(value))
        self.writeConfig()

    @property
    def export_sameColX(self):
        return self.config.getint('settings', 'export_sameColX')
    @export_sameColX.setter
    def export_sameColX(self, value):
        self.config.set('settings', 'export_sameColX', str(value))
        self.writeConfig()

    @property
    def export_datasetFormat(self):
        return self.config.get('settings', 'export_datasetFormat')
    @export_datasetFormat.setter
    def export_datasetFormat(self, datasetformat):
        self.config.set('settings', 'export_datasetFormat', datasetformat)
        self.writeConfig()
    
    @property
    def export_datasetDir(self):
        return self.config.get('settings', 'export_datasetDir')
    @export_datasetDir.setter
    def export_datasetDir(self, path):
        self.config.set('settings', 'export_datasetDir', path)
        self.writeConfig()

    def _initialReadConfig(self):
        if not os.path.exists(self.configpath):
            # initial creation
            if os.path.exists('.tda'):
                shutil.rmtree('.tda') # remove all
            os.makedirs('.tda')
            os.makedirs(self.selectedImgDir)

            # default value
            default = {
                'lastOpenDir': path_desktop(),
                'credentialJsonpath': None,

                'export_defaultFileFormat': 'CSV',
                'export_sameRowY': 50,
                'export_sameColX': 15,
                
                'export_datasetFormat': 'VOC',
                'export_datasetDir': None
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