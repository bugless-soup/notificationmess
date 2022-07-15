from functools import cached_property
from typing import overload

from notificationmess.graphics.shapes import Vector2D
from notificationmess.graphics.shapes.transform import IDENTITY_MATRIX, Transform
from notificationmess.graphics.shapes.point import Point
from notificationmess.graphics.shapes.transforms import Translation, Rotation, HorizontalShearing, Scaling


class Square(tuple):
    def __new__(cls, a, b=None, c=None, d=None, e=None, f=None):
        if f is not None:
            return tuple.__new__(Square, (Point(a, b), Point(c, d), Point(e, f)))
        elif c is not None:
            return tuple.__new__(Square, (Point(p) for p in (a, b, c)))
        else:
            return tuple.__new__(Square, (Point(p) for p in a))

    @overload
    def __init__(self, tl_x: float, tl_y: float, tr_x: float, tr_y: float, br_x: float, br_y: float):
        ...

    @overload
    def __init__(self,
                 top_left: Vector2D,
                 top_right: Vector2D,
                 bottom_right: Vector2D):
        ...

    @overload
    def __init__(self, vertices: list[Vector2D]):
        ...

    def __init__(self, *args):
        pass

    @property
    def top_left(self) -> Point:
        return self[0]

    @property
    def top_right(self) -> Point:
        return self[1]

    @property
    def bottom_right(self) -> Point:
        return self[2]

    @cached_property
    def size(self):
        bbox = [0] * 4
        for p in (self.top_left,
                  self.top_right,
                  self.bottom_right,
                  self.top_left - self.top_right + self.bottom_right):
            if p[0] < bbox[0]:
                bbox[0] = p[0]
            elif p[0] > bbox[2]:
                bbox[2] = p[0]
            if p[1] < bbox[1]:
                bbox[1] = p[1]
            elif p[1] > bbox[3]:
                bbox[3] = p[1]
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    def apply(self, transformation: Transform) -> 'Square':
        return Square(*[point.apply(transformation) for point in self])

    def get_transform(self, initial_size: Vector2D):
        final = IDENTITY_MATRIX
        square = self
        for condition, transformation in [
            (lambda: square.top_left != Point((0, 0)), lambda: Translation(square.top_left)),
            (lambda: square.top_right.y != 0, lambda: Rotation(square.top_right)),
            (lambda: square.top_right.x != square.bottom_right.x,
             lambda: HorizontalShearing(square.top_right, square.bottom_right)),
            (lambda: square.bottom_right != Point(initial_size),
             lambda: Scaling(square.bottom_right / initial_size))
        ]:
            if condition():
                current: Transform = transformation()
                final = current.then(final)
                square = square.apply(-current)
        return final

    def get_transform_no_scale(self):
        final = IDENTITY_MATRIX
        square = self
        for condition, transformation in (
            (lambda: square.top_left != Point((0, 0)), lambda: Translation(square.top_left)),
            (lambda: square.top_right.y != 0, lambda: Rotation(square.top_right)),
            (lambda: square.top_right.x != square.bottom_right.x,
             lambda: HorizontalShearing(square.top_right, square.bottom_right))
        ):
            if condition():
                current: Transform = transformation()
                final = current.then(final)
                square = square.apply(-current)
        return square, final

    def __iter__(self):
        return iter([self.top_left, self.top_right, self.bottom_right])

    def __str__(self):
        return str(list(self))
