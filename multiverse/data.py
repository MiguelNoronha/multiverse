from dataclasses import dataclass

from multiverse.constants import DEGREE_TO_ORIENTATION, ORIENTATION_TO_DEGREE


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, vector):
        if not isinstance(vector, Position):
            raise TypeError("A Position can only be added to another Position")

        return Position(self.x + vector.x, self.y + vector.y)

    def __iadd__(self, vector):
        if not isinstance(vector, Position):
            raise TypeError("A Position can only be added to another Position")

        self.x += vector.x
        self.y += vector.y
        return self

    @property
    def tuple(self):
        return self.x, self.y


@dataclass
class Orientation:
    degree: int

    def __init__(self, degree):
        if isinstance(degree, str):
            degree = ORIENTATION_TO_DEGREE[degree]
        self.degree = degree

    def __add__(self, other):
        if not isinstance(other, Orientation):
            raise TypeError("An Orientation can only be added to another Orientation")

        return Orientation((self.degree + getattr(other, "degree", other)) % 360)

    def __iadd__(self, other):
        if not isinstance(other, Orientation):
            raise TypeError("An Orientation can only be added to another Orientation")

        self.degree = (self.degree + getattr(other, "degree", other)) % 360
        return self

    def __str__(self):
        return DEGREE_TO_ORIENTATION[self.degree]