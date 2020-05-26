import numpy as np


def calculate(a, b, c):
    x = np.arange(-1, 3, 0.01)
    y = [float(a) * (x_elem**2) + float(b) * x_elem + float(c) for x_elem in x]
    return [x, y]
