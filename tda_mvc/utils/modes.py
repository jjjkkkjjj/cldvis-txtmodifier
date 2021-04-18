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
    CSV = 'CSV', 'csv'
    EXCEL = 'EXCEL', 'xlsx'
    TSV = 'TSV', 'tsv'
    PSV = 'PSV', 'psv'


    @staticmethod
    def gen_list():
        return [m.value[0] for m in ExportFileExtention]

    @staticmethod
    def get_index(val):
        return ExportFileExtention.gen_list().index(val)

    @staticmethod
    def gen_filters_args(val=None):
        if val:
            ind = ExportFileExtention.get_index(val)
            filters_list = [(m.value[0], m.value[1]) for m in ExportFileExtention]
            return filters_list[ind:] + filters_list[:ind]
        else:
            return [(m.value[0], m.value[1]) for m in ExportFileExtention]

class ExportDatasetFormat(Enum):
    VOC = 'VOC', 'xml'

    @staticmethod
    def gen_list():
        return [m.value[0] for m in ExportDatasetFormat]

    @staticmethod
    def get_index(val):
        return ExportDatasetFormat.gen_list().index(val)

    @staticmethod
    def gen_filters_args(val=None):
        if val:
            ind = ExportDatasetFormat.get_index(val)
            filters_list = [(m.value[0], m.value[1]) for m in ExportDatasetFormat]
            return filters_list[ind:] + filters_list[:ind]
        else:
            return [(m.value[0], m.value[1]) for m in ExportDatasetFormat]

