from typing import overload, Union

import numpy as np

from notificationmess.graphics.shapes.point import Point
from notificationmess.graphics.shapes.transform import Transform


class Translation(Transform):
    def __init__(self, delta: Point):
        self.delta = delta
        super().__init__([
            [1, 0, self.delta.x],
            [0, 1, self.delta.y],
            [0, 0, 1]])

    def __neg__(self):
        return Translation(-self.delta)

    def __str__(self):
        return "Translation: " + str(self.delta)


class Rotation(Transform):
    @overload
    def __init__(self, phase: float, pivot: Point = None):
        ...

    @overload
    def __init__(self, point: Point):
        ...

    def __init__(self,
                 phase_or_point: Union[float, Point],
                 pivot: Point = None):
        if pivot is not None:
            self.phase = phase_or_point
            self.pivot = pivot
        elif isinstance(phase_or_point, Point):
            self.phase = phase_or_point.phase
            self.pivot = Point((0, 0))
        else:
            self.phase = phase_or_point
            self.pivot = Point((0, 0))
        super().__init__(Translation(-self.pivot).then([
            [np.cos(self.phase), -np.sin(self.phase), 0],
            [np.sin(self.phase), np.cos(self.phase), 0],
            [0, 0, 1]
        ]).then(Translation(self.pivot)))

    def __neg__(self):
        return Rotation(-self.phase, self.pivot)

    def __str__(self):
        return "Rotation: " + str(self.phase / np.pi) + " * pi\n" + \
               "Around: " + str(self.pivot)


class HorizontalShearing(Transform):
    @overload
    def __init__(self, coefficient: float):
        ...

    @overload
    def __init__(self, base: Point, target: Point):
        ...

    def __init__(self, coefficient_or_base: Union[float, Point], target: Point = None):
        if target is not None:
            self.coefficient = (target.x - coefficient_or_base.x) / (target.y - coefficient_or_base.y)
        else:
            self.coefficient = coefficient_or_base
        super().__init__([
            [1, self.coefficient, 0],
            [0, 1, 0],
            [0, 0, 1]])

    def __neg__(self):
        return HorizontalShearing(-self.coefficient)

    def __str__(self):
        return "HorizontalShearing: " + str(self.coefficient)


class VerticalShearing(Transform):
    @overload
    def __init__(self, coefficient: float):
        ...

    @overload
    def __init__(self, base: Point, target: Point):
        ...

    def __init__(self, coefficient_or_base: Union[float, Point], target: Point = None):
        if target is not None:
            self.coefficient = (target.y - coefficient_or_base.y) / (target.x - coefficient_or_base.x)
        else:
            self.coefficient = coefficient_or_base
        super().__init__([
            [1, 0, 0],
            [self.coefficient, 1, 0],
            [0, 0, 1]])

    def __neg__(self):
        return HorizontalShearing(-self.coefficient)

    def __str__(self):
        return "HorizontalShearing: " + str(self.coefficient)


class Scaling(Transform):
    def __init__(self, delta: Point):
        self.delta = delta
        super().__init__([
            [self.delta.x, 0, 0],
            [0, self.delta.y, 0],
            [0, 0, 1]])

    def __neg__(self):
        return Scaling(1 / self.delta)

    def __str__(self):
        return "Scaling: " + str(self.delta)
