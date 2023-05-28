from __future__ import annotations
from threedeebeetree import Point


def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
    """
    Time complexity: O(n log n), where n is the number of points in the points list,
    as it performs a sorting operation using the sort method, which has a complexity of O(n log n).
    """
    # Define helper function for sorting and partitioning a list of points
    def sort_and_partition(points: List[Point], axis: int) -> List[Point]:
        """
        Time complexity: O(n log n),
        as it calls the sort_and_partition function three times,
        passing the entire my_coordinate_list as the points parameter,
        resulting in a complexity of O(n log n) for each call.
        """
        points.sort(key=lambda point: point[axis])
        result = []

        def build_tree_rec(lo, hi):
            if hi - lo < 1:
                return
            # Add median
            mid = (hi + lo) // 2
            result.append(points[mid])
            build_tree_rec(lo, mid)
            build_tree_rec(mid + 1, hi)

        build_tree_rec(0, len(points))
        return result

    # Create ordering for each axis
    x_ordered = sort_and_partition(my_coordinate_list, 0)
    y_ordered = sort_and_partition(my_coordinate_list, 1)
    z_ordered = sort_and_partition(my_coordinate_list, 2)

    # Combine the orderings to satisfy the splitting condition
    final_ordering = []
    for i in range(len(x_ordered)):
        final_ordering.append(x_ordered[i])
        final_ordering.append(y_ordered[i])
        final_ordering.append(z_ordered[i])

    return final_ordering
