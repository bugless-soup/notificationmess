from functools import cache
from typing import Union

from numpy import ndarray, float32, linalg


class Transform:
    matrix: ndarray

    def __init__(self, matrix: Union['Transform', list[list[float]]]):
        self.matrix = matrix.matrix if isinstance(matrix, Transform) else float32(matrix)

    @cache
    def to_pil_data(self):
        m = linalg.inv(self.matrix)
        return [
            float(c)
            for c in (m[0, 0], m[0, 1], m[0, 2], m[1, 0], m[1, 1], m[1, 2])
        ]

    def then(self, other: Union['Transform', list[list[float]]]):
        if isinstance(other, list):
            other = Transform(other)
        return Transform(other.matrix.dot(self.matrix))

    def __neg__(self):
        raise NotImplementedError


IDENTITY_MATRIX = Transform([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]])
