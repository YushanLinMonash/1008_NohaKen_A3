from dataclasses import dataclass
from heap import MaxHeap


@dataclass
class Beehive:
    """A beehive has a position in 3d space, and some stats."""

    x: int
    y: int
    z: int

    capacity: int
    nutrient_factor: int
    volume: int = 0


class BeehiveSelector:

    def __init__(self, max_beehives: int):
        """
        O(1)
        This function just sets some variables.
        It operates in constant time.
        """
        self.max_beehives = max_beehives
        self.beehives = MaxHeap(max_beehives)

    def set_all_beehives(self, hive_list: list[Beehive]):
        """
        set_all_beehives should replace all current (possibly none)
        beehives in the selector with the beehives in the list provided as an argument.
        This function clears the existing heap and then iterates through the hive_list to add each hive into the heap.
        The complexity is O(n), where n is the number of items in hive_list.
        """
        # Empty the heap
        while len(self.beehives) > 0:
            self.beehives.get_max()

        # Add all beehives from the list to the heap
        for hive in hive_list:
            self.add_beehive(hive)

    def add_beehive(self, hive: Beehive):
        """
        this is to add the beehive into the MaxHeap
        O(log m)
        This function adds a new beehive into the heap,
        which is a log operation. The complexity is O(log m),
        where m is the size of the heap (the number of beehives currently in the selector).
        """
        value = min(hive.capacity, hive.volume) * hive.nutrient_factor
        if len(self.beehives) < self.max_beehives:
            self.beehives.add((value, hive))
        else:
            min_value, _ = self.beehives.get_max()
            if value > min_value:
                self.beehives.add((value, hive))

    def harvest_best_beehive(self)-> float:
        """
        select the largest value beehive from the heap
        the largest value is  min(Capacity, Volume) * nutrient_factor
        O(log m)
        This function pops the maximum element from the heap,
        which is a log operation. The complexity is O(log m),
        where m is the size of the heap (the number of beehives currently in the selector).
        """
        if len(self.beehives) == 0:
            return 0.0
        else:
            # Pop the hive with the maximum value and return its value.
            _, best_hive = self.beehives.get_max()
            return min(best_hive.capacity, best_hive.volume) * best_hive.nutrient_factor