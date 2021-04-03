from enum import Enum

class PredictionMode(Enum):
    IMAGE = 'image'
    TABLE = 'table'

    @staticmethod
    def gen_list():
        return [m.value for m in PredictionMode]