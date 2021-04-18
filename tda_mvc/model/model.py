from .file import FileModelMixin
from .prediction import PredictionModelMixin
from .viewer import ViewerModelMixin
from .annotation import AnnotationModelMixin
from .config import Config


class _BaseModel(object):
    def __init__(self):
        pass

class Model(FileModelMixin, ViewerModelMixin, PredictionModelMixin, AnnotationModelMixin, _BaseModel):
    """
    Singleton class
    """
    config = Config()

    def __init__(self):
        FileModelMixin.__init__(self)
        ViewerModelMixin.__init__(self)
        PredictionModelMixin.__init__(self)
        AnnotationModelMixin.__init__(self)

    def discardAll(self):
        self.discard_area()
        self.discard_annotations()