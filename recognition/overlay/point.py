from __future__ import annotations
import math


class Point:
    """
    Класс, описывающий точку на изображении, и реализующий необходимые методы для работы
    с ней
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = f'Point: {self.x, self.y}'
        self.cv2_coords = (self.y, self.x)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def distance(self, other: Point):
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        return math.hypot(dx, dy)
