import os

def check_instance(name, val, cls, allow_none=True):
    if allow_none and val is None:
        return val

    if not isinstance(val, cls):
        if isinstance(cls, (list, tuple)):
            clsnames = [c.__name__ for c in cls]
            raise ValueError('Invalid argument: \'{}\' must be {}, but got {}'.format(name, clsnames, type(val).__name__))
        else:
            raise ValueError('Invalid argument: \'{}\' must be {}, but got {}'.format(name, cls.__name__, type(val).__name__))

    return val

def path_desktop():
    return os.path.join(os.path.expanduser('~'), 'Desktop')