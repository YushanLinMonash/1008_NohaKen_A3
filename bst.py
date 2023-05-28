""" Binary Search Tree ADT.
    Defines a Binary Search Tree with linked nodes.
    Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Alexey Ignatiev, further modified by Jackson Goerner'
__docformat__ = 'reStructuredText'

from typing import TypeVar, Generic
from node import TreeNode
import sys

# generic types
K = TypeVar('K')
I = TypeVar('I')
T = TypeVar('T')


class BinarySearchTree(Generic[K, I]):
    """ Basic binary search tree. """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the bst is empty
            :complexity: O(1)
        """
        return self.root is None

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """
        # O(1) - Returning the length

        return self.length

    def __contains__(self, key: K) -> bool:
        """
            Checks to see if the key is in the BST
            :complexity: see __getitem__(self, key: K) -> (K, I)
        """
        # O(D), where D is the depth of the tree. This is because this method uses
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: K) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
            :complexity best: O(CompK) finds the item in the root of the tree
            :complexity worst: O(CompK * D) item is not found, where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        # O(D), where D is the depth of the tree. This method performs a search through the tree to find the given key.
        return self.get_tree_node_by_key(key).item

    def get_tree_node_by_key(self, key: K) -> TreeNode:
        # O(D), where D is the depth of the tree.
        # This is because it relies on get_tree_node_by_key_aux which performs a search through the tree.
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current: TreeNode, key: K) -> TreeNode:
        # O(D), where D is the depth of the tree. It performs a search through the tree to find the given key.
        if current is None:
            raise KeyError('Key not found: {0}'.format(key))
        elif key == current.key:
            return current
        elif key < current.key:
            return self.get_tree_node_by_key_aux(current.left, key)
        else:  # key > current.key
            return self.get_tree_node_by_key_aux(current.right, key)

    def __setitem__(self, key: K, item: I) -> None:
        # O(D), where D is the depth of the tree.
        # This method attempts to insert an item into the tree, which involves traversing the tree.
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: TreeNode, key: K, item: I) -> TreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            :complexity best: O(CompK) inserts the item at the root.
            :complexity worst: O(CompK * D) inserting at the bottom of the tree
            where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        if current is None:  # base case: at the leaf
            current = TreeNode(key, item=item)
            self.length += 1
            current.subtree_size = 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
            current.subtree_size += 1
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
            current.subtree_size += 1
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        return current

    def __delitem__(self, key: K) -> None:
        # O(D), where D is the depth of the tree.
        # This method deletes an item from the tree, which involves traversing the tree.
        self.root = self.delete_aux(self.root, key)

    def delete_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.
            O(D), where D is the depth of the tree.
            This method is responsible for the actual deletion operation, which involves traversing the tree and finding the successor in some cases.
        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
            current.subtree_size += 1
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
            current.subtree_size += 1
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                current.subtree_size = 1
                return None
            elif current.left is None:
                self.length -= 1
                current.subtree_size = 1
                return current.right
            elif current.right is None:
                self.length -= 1
                current.subtree_size = 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        return current

    def get_successor(self, current: TreeNode) -> TreeNode:
        """
            Get successor of the current node.
            It should be a child node having the smallest key among all the
            larger keys.
             O(D), where D is the depth of the tree.
             This method finds the successor of a node, which may involve traversing down the right subtree.
        """
        if current is None or current.right is None:
            return None
        else:
            successor = self.get_minimal(current.right)

        if successor.key > current.key:
            return successor
        else:
            return None

    def get_minimal(self, current: TreeNode) -> TreeNode:
        """
            Get a node having the smallest key in the current sub-tree.
            get_minimal should return, given some subtree node current, the smallest key node in the subtree rooted at current.
            O(D), where D is the depth of the tree.
            This method finds the node with the smallest key in a subtree, which involves traversing down the left subtree.
        """
        if current is None:
            return None
        if current.left is None:
            return current
        return self.get_minimal(current.left)

    def is_leaf(self, current: TreeNode) -> bool:
        """
        Simple check whether or not the node is a leaf.
         O(1) - Just checking if the left and right child of a node are None
        """
        return current.left is None and current.right is None

    def draw(self, to=sys.stdout):
        """
        Draw the tree in the terminal.
        O(n), where n is the number of nodes in the tree. This method prints out every node in the tree.
        """

        # get the nodes of the graph to draw recursively
        self.draw_aux(self.root, prefix='', final='', to=to)

    def draw_aux(self, current: TreeNode, prefix='', final='', to=sys.stdout) -> K:
        """
        Draw a node and then its children.
         O(n), where n is the number of nodes in the tree.
         This method recursively traverses and prints every node in the tree.
        """

        if current is not None:
            real_prefix = prefix[:-2] + final
            print('{0}{1}'.format(real_prefix, str(current.key)), file=to)

            if current.left or current.right:
                self.draw_aux(current.left, prefix=prefix + '\u2551 ', final='\u255f\u2500', to=to)
                self.draw_aux(current.right, prefix=prefix + '  ', final='\u2559\u2500', to=to)
        else:
            real_prefix = prefix[:-2] + final
            print('{0}'.format(real_prefix), file=to)

    def kth_smallest(self, k: int, current: TreeNode) -> TreeNode:
        """
        Finds the kth smallest value by key in the subtree rooted at current.
        O(D), where D is the depth of the tree.
        This method performs a modified search operation, which involves traversing the tree.
        """
        left_size = current.left.subtree_size if current.left else 0

        if k - 1 == left_size:  # current is the kth smallest
            return current
        elif k <= left_size:  # the kth smallest is in the left subtree
            return self.kth_smallest(k, current.left)
        else:  # the kth smallest is in the right subtree
            return self.kth_smallest(k - left_size - 1, current.right)
