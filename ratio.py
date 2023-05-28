from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil
from bst import BinarySearchTree

T = TypeVar("T")
I = TypeVar("I")


class Percentiles(Generic[T]):

    def __init__(self) -> None:
        self.points = []

    def add_point(self, item: T):
        self.points.append(item)
        self.points.sort()

    def remove_point(self, item: T):
        if item in self.points:
            self.points.remove(item)

    def ratio(self, x, y):
        if not (0 <= x <= 100 and 0 <= y <= 100):
            raise ValueError("Invalid values. x and y must be between 0 and 100.")

        n = len(self.points)
        larger_than = ceil(n * (x / 100))
        smaller_than = ceil(n * (y / 100))

        return self.points[larger_than:n - smaller_than]


if __name__ == "__main__":
    points = list(range(50))
    import random

    random.shuffle(points)
    p = Percentiles()
    for point in points:
        p.add_point(point)
    # Numbers from 8 to 16.
    print(p.ratio(15, 66))
