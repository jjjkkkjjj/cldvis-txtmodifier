from enum import Enum


class ContextActionType(Enum):
    REMOVE_ANNOTATION = 0
    DUPLICATE_ANNOTATION = 1
    REMOVE_POINT = 2
    DUPLICATE_POINT = 3


class RubberMode(Enum):
    SELECTION = 0
    PREDICTION = 1

class MoveActionState(Enum):
    CREATE = 0
    RESIZE = 1
    MOVE = 2