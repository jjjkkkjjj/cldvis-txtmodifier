from ..utils.modes import PredictionMode
from .base import VCAbstractMixin

class CentralVCMixin(VCAbstractMixin):

    @property
    def imageView(self):
        return self.central.imageView

    def establish_connection(self):
        self.imageView.areaChanged.connect(self.areaChanged)

    def areaChanged(self):
        self.leftdock.updateUI()
        self.menu.updateUI()