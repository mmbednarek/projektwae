import numpy as np

def get_error(result, expected):
    return np.linalg.norm(np.asarray(expected) - np.asarray(result))

def as_handler(func):
    return lambda args: func(*args)
