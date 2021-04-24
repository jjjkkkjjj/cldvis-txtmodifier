import numpy as np

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

    def load_from_tda(self, tda):
        """
        Load model params from .tda
        Note that parentVals will not be called. So you should call parentVals in viewcontroller properly.
        :param tda:
        :return:
        """
        from .tda import TDA
        from ..utils.modes import AreaMode, PredictionMode
        tda: TDA

        # default tda name
        self.default_savename = getattr(tda, 'default_savename', '')

        # the reason of using getattr is for changing TDA contents
        self.areamode = getattr(tda, 'areamode', AreaMode.RECTANGLE)
        self.predmode = getattr(tda, 'predmode', PredictionMode.IMAGE)

        # area
        percent_pts = getattr(tda, 'rectangle_percent_pts', None)
        if percent_pts is not None:
            self.rectangle.set_percent_points(percent_pts)
        percent_pts = getattr(tda, 'quadrangle_percent_pts', None)
        if percent_pts is not None:
            self.quadrangle.set_percent_points(percent_pts)
        percent_pts = getattr(tda, 'predictedArea_percent_pts', None)
        if percent_pts is not None:
            self.predictedArea.set_percent_points(percent_pts)

        # annotation
        self.results = getattr(tda, 'results_dict', {})
