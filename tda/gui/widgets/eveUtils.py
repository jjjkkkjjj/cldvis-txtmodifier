from enum import Enum


class ContextActionType(Enum):
    REMOVE_ANNOTATION = 0
    DUPLICATE_ANNOTATION = 1
    REMOVE_POINT = 2
    DUPLICATE_POINT = 3


class AreaMode(Enum):
    SELECTION = 0
    PREDICTION = 1

class MoveActionState(Enum):
    CREATE = 0
    RESIZE = 1
    MOVE = 2

class PredictionMode(Enum):
    IMAGE = 'image'
    TABLE = 'table'

    @staticmethod
    def gen_list():
        return [m.value for m in PredictionMode]
