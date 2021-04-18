from enum import Enum

class PredictionMode(Enum):
    IMAGE = 'image'
    DOCUMENT = 'document'

    @staticmethod
    def gen_list():
        return [m.value for m in PredictionMode]

class ShowingMode(Enum):
    ENTIRE = 'entire'
    SELECTED = 'selected'

class AreaMode(Enum):
    RECTANGLE = 'rectangle'
    QUADRANGLE = 'quadrangle'

class MoveActionState(Enum):
    CREATE = 0
    RESIZE = 1
    MOVE = 2

class ExportFileExtention(Enum):
    CSV = 'csv'
    EXCEL = 'excel'
    TSV = 'tsv'
    PSV = 'psv'

    @staticmethod
    def gen_list():
        return [m.value for m in ExportFileExtention]