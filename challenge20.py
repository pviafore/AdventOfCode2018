"""
    Advent of Code Day 20
"""
from operator import itemgetter
from typing import Set
from common.graph import Graph
from common.grid import Point, to_above, to_below, to_left, to_right
from common.input_file import read_single_line


def get_next_point(character: str, point: Point) -> Point:
    """
        Get the next point based on NESW
    """
    return {
        "N": to_above,
        "S": to_below,
        "W": to_left,
        "E": to_right
    }[character](point)

class Map:
    """
        A map of the cave system
    """
    def __init__(self, regex):
        self.graph = Graph()
        self.origin = Point(0, 0)
        self.parse_regex(regex, set([self.origin]))

    def parse_regex(self, regex: str, nodes: Set[Point]) -> Set[Point]:
        """
            Parse the regular expression filtering out (|)
        """
        parens_stack = []
        next_points: Set[Point] = set()
        for index, character in enumerate(regex):
            if character == "(":
                parens_stack.append(index)
                next_points = set()
            elif character == ")":
                start = parens_stack.pop()
                if not parens_stack:
                    nodes = next_points | self.parse_regex(regex[start + 1:index], nodes)
            elif len(parens_stack) == 1 and character == "|":
                start = parens_stack.pop()
                next_points = next_points | self.parse_regex(regex[start + 1: index], nodes)
                parens_stack.append(index)
            elif not parens_stack:
                for node in nodes:
                    self.graph.add_edge(node, get_next_point(character, node))
                nodes = {get_next_point(character, node) for node in nodes}

        assert parens_stack == []
        return nodes

    def get_max_distance(self) -> int:
        """
            Get the maximum distance from the origin
        """
        return max(self.graph.get_node_distances(self.origin), key=itemgetter(0))[0]

    def get_number_of_rooms_at_least_distance_away(self, distance: int) -> int:
        """
            Get the number of rooms at least a certain distance away
        """
        return len([_ for d, _ in self.graph.get_node_distances(self.origin) if d >= distance])

REGEX = read_single_line("input/input20.txt")
assert REGEX[0] == "^" and REGEX[-1] == "$"
CAVE = Map(REGEX[1:-1])
print(CAVE.get_max_distance())
print(CAVE.get_number_of_rooms_at_least_distance_away(1000))
