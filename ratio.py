from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil
from bst import BinarySearchTree

T = TypeVar("T")
I = TypeVar("I")


class Percentiles(Generic[T]):

    def __init__(self) -> None:
        """
        Initializes an instance of the Percentiles class with an empty list of points.
        O(1) - Just initializing an empty list.
        """
        self.points = []

    def add_point(self, item: T):
        """
        Adds a new point to the list of points and sorts the list in ascending order
        O(n log n), where n is the number of points.
        Appending an item to a list is an O(1) operation, but sorting the list afterwards takes O(n log n) time.
        """
        self.points.append(item)
        self.points.sort()

    def remove_point(self, item: T):
        """
        Removes a specified point from the list of points if it exists in the list
        O(n), where n is the number of points.
        Checking if an item is in a list and removing it both require traversing the entire list in the worst case.
        """
        if item in self.points:
            self.points.remove(item)

    def ratio(self, x, y):
        """
        Returns a slice of the sorted list of points,
        including all points that are larger than a certain percentile and smaller than another percentile.
        The percentiles are specified as parameters.
        O(1) - Calculating the indices for slicing the list and slicing the list both require constant time.
        However, this is assuming that the list is already sorted, as the
        """
        if not (0 <= x <= 100 or 0 <= y <= 100):
            raise ValueError("Invalid value.")

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
