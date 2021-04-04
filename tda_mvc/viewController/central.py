from ..utils.modes import PredictionMode
from .base import VCAbstractMixin

class CentralVCMixin(VCAbstractMixin):

    @property
    def imageView(self):
        return self.central.imageView

    def establish_connection(self):
        self.imageView.areaChanged.connect(self.areaChanged)

    def areaChanged(self):
        if self.model.predmode == PredictionMode.IMAGE:
            self.model.saveSelectedImg_imagemode(self.model.imgpath)
        elif self.model.predmode == PredictionMode.TABLE:
            self.model.saveSelectedImg_tablemode(self.model.imgpath)

        self.leftdock.updateUI()
        self.menu.updateUI()