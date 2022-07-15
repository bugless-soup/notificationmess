from typing import TypeVar

from notificationmess.graphics.shapes import Vector2D
from notificationmess.graphics.shapes.point import Point
from notificationmess.graphics.shapes.transform import Transform
from notificationmess.graphics.shapes.transforms import Scaling

T = TypeVar('T')


class Transformable:
    def __init__(self, size: Vector2D):
        self.size = size

    def apply(self: T, transform: Transform) -> T:
        raise NotImplementedError

    def scale(self, x: float, y: float):
        return self.apply(Scaling(Point((x, y))))

    def scale_to(self, width: float, height: float):
        return self.apply(Scaling(Point((width, height)) / Point(self.size)))
