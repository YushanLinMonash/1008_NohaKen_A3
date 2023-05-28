from __future__ import annotations
from typing import Generic, TypeVar, Tuple
from dataclasses import dataclass, field

I = TypeVar('I')
Point = Tuple[int, int, int]


@dataclass
class BeeNode:
    key: Point
    item: I
    Octant1: BeeNode | None = None
    Octant2: BeeNode | None = None
    Octant3: BeeNode | None = None
    Octant4: BeeNode | None = None
    Octant5: BeeNode | None = None
    Octant6: BeeNode | None = None
    Octant7: BeeNode | None = None
    Octant8: BeeNode | None = None
    subtree_size: int = 1

    def get_child_for_key(self, point: Point) -> BeeNode | None:
        x0, y0, z0 = self.key
        x, y, z = point

        if x < x0:
            if y < y0:
                return self.Octant1 if z < z0 else self.Octant2
            else:
                return self.Octant3 if z < z0 else self.Octant4
        else:
            if y < y0:
                return self.Octant5 if z < z0 else self.Octant6
            else:
                return self.Octant7 if z < z0 else self.Octant8


class ThreeDeeBeeTree(Generic[I]):
    """ 3️⃣🇩🐝🌳 tree. """

    def __init__(self) -> None:
        """
            Initialises an empty 3DBT
        """
        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the 3DBT is empty
        """
        return len(self) == 0

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.length

    def __contains__(self, key: Point) -> bool:
        """
            Checks to see if the key is in the 3DBT
        """
        try:
            self.get_tree_node_by_key(key)
            return True
        except KeyError:
            return False

    def __getitem__(self, key: Point) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
        """
        node = self.get_tree_node_by_key(key)
        return node.item

    def get_tree_node_by_key(self, key: Point) -> BeeNode:
        current = self.root
        while current is not None:
            if current.key == key:
                return current
            else:
                current = current.get_child_for_key(key)
        raise KeyError("Key not found")

    def __setitem__(self, key: Point, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: BeeNode, key: Point, item: I) -> BeeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
        """
        if current is None:
            self.length += 1
            return BeeNode(key=key, item=item)

        x0, y0, z0 = current.key
        x, y, z = key

        if x < x0:
            if y < y0:
                if z < z0:
                    current.Octant1 = self.insert_aux(current.Octant1, key, item)
                else:
                    current.Octant2 = self.insert_aux(current.Octant2, key, item)
            else:
                if z < z0:
                    current.Octant3 = self.insert_aux(current.Octant3, key, item)
                else:
                    current.Octant4 = self.insert_aux(current.Octant4, key, item)
        else:
            if y < y0:
                if z < z0:
                    current.Octant5 = self.insert_aux(current.Octant5, key, item)
                else:
                    current.Octant6 = self.insert_aux(current.Octant6, key, item)
            else:
                if z < z0:
                    current.Octant7 = self.insert_aux(current.Octant7, key, item)
                else:
                    current.Octant8 = self.insert_aux(current.Octant8, key, item)

        current.subtree_size += 1
        return current

    def is_leaf(self, current: BeeNode) -> bool:
        """ Simple check whether the node is a leaf. """
        if current.Octant1 and \
                current.Octant2 and \
                current.Octant3 and \
                current.Octant4 and \
                current.Octant5 and \
                current.Octant6 and \
                current.Octant7 and \
                current.Octant8 is None:
            return True
        else:
            return False


if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"
    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size)  # 2
