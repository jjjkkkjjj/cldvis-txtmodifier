from .file import FileModelMixin
from .vision import VisionModelMixin
from .config import Config


class _BaseModel(object):
    def __init__(self):
        pass

class Model(FileModelMixin, VisionModelMixin, _BaseModel):
    """
    Singleton class
    """
    config = Config()

    def __init__(self):
        FileModelMixin.__init__(self)
        VisionModelMixin.__init__(self)