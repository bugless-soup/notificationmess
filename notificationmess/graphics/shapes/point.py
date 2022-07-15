from functools import cached_property
from typing import overload

import numpy as np
from numpy import float32

from notificationmess.graphics.shapes import Vector2D
from notificationmess.graphics.shapes.transform import Transform


class Point(tuple):
    def __new__(cls, x, y: float = None):
        return tuple.__new__(Point, x if y is None else (x, y))

    @overload
    def __init__(self, position: Vector2D):
        ...

    @overload
    def __init__(self, point: 'Point'):
        ...

    @overload
    def __init__(self, x: float, y: float):
        ...

    def __init__(self, *args):
        pass

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @cached_property
    def vector(self):
        return float32([[self.x], [self.y], [1]])

    @cached_property
    def magnitude(self):
        return np.sqrt(self.x ** 2 + self.y ** 2)

    @cached_property
    def phase(self):
        return np.arccos(self.x / self.magnitude) * np.sign(self.y)

    def apply(self, transform: Transform):
        point = transform.matrix.dot(self.vector)
        return Point(point[0, 0], point[1, 0])

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return Point(other / self.x, other / self.y)
        else:
            return Point(other[0] / self.x, other[1] / self.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Point(self.x * other, self.y * other)
        else:
            return Point(self.x * other[0], self.y * other[1])

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Point(self.x / other, self.y / other)
        else:
            return Point(self.x / other[0], self.y / other[1])

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Point(self.x + other, self.y + other)
        else:
            return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Point(self.x - other, self.y - other)
        else:
            return Point(self.x - other[0], self.y - other[1])
