from enum import Enum

class PredictionMode(Enum):
    IMAGE = 'image'
    TABLE = 'table'

    @staticmethod
    def gen_list():
        return [m.value for m in PredictionMode]

class ShowingMode(Enum):
    ENTIRE = 'entire'
    SELECTED = 'selected'

class MoveActionState(Enum):
    CREATE = 0
    RESIZE = 1
    MOVE = 2