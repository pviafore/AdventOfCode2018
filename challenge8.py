"""
    Advent of Code 2018
"""

from common.input_file import read_single_line
class Tree:
    """
        A simple recrusive tree structure
    """
    def __init__(self):
        """
            Constructor
        """
        self.metadata = []
        self.children = []

    def get_metadata_sum(self):
        """
            Gets the sum of all metadata and all children's metdata
        """
        return sum(self.metadata) + sum(child.get_metadata_sum() for child in self.children)


    def get_value(self):
        """
            Get the value (sum of metadata if no children), otherwise sum of
            children based on metadata
        """
        if not self.children:
            return sum(self.metadata)
        indices = [index - 1 for index in self.metadata if self.is_valid_child_index(index)]
        values = [self.children[i].get_value() for i in indices]
        return sum(values)

    def is_valid_child_index(self, index):
        """
            Return if the 1 based index is greater than zero,
            but can index into the children
        """
        return 0 < index <= len(self.children)


def create_tree(tree_iter):
    """
        Create a tree
    """
    num_children, num_metadata, = next(tree_iter), next(tree_iter)
    assert num_metadata > 0
    tree = Tree()
    tree.children = [create_tree(tree_iter) for _ in range(num_children)]
    tree.metadata = [next(tree_iter) for _ in range(num_metadata)]
    return tree

TREE_INPUT = read_single_line("input/input8.txt")
TREE = create_tree(iter(map(int, TREE_INPUT.split())))
if __name__ == "__main__":

    print(TREE.get_metadata_sum())
    print(TREE.get_value())
