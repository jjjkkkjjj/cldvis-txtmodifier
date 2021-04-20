import pickle

class TDA(object):
    """
    This object is for .tda
    """
    def __init__(self, model):
        from .model import Model
        model: Model

        self.rectangle_percent_pts = model.rectangle.percent_points
        self.quadrangle_percent_pts = model.quadrangle.percent_points
        self.predictedArea_percent_pts = model.predictedArea.percent_points
        self.results_dict = model.annotations.to_dict()
        self.areamode = model.areamode
        self.predmode = model.predmode
        self.default_tdaname = model.default_tdaname

    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path):
        with open(path, 'rb') as f:
            tda = pickle.load(f)
            return tda
