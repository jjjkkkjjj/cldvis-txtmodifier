
from .base import ModelAbstractMixin

class ViewerModelMixin(ModelAbstractMixin):
    def __init__(self):
        self.zoomvalue = 100

    @property
    def isZoomOutable(self):
        return self.zoomvalue >= 20 + 10
    @property
    def isZoomInable(self):
        return self.zoomvalue <= 190 - 10