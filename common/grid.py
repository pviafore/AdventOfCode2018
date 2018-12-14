"""
    A module containing Points and Grids
"""
# we don't want to change x, y names because those are actually good names
# pylint: disable=invalid-name
from collections import abc, namedtuple
from itertools import product
from typing import Iterable, List

Point = namedtuple("Point", ["x", "y"])

def to_point(point_str: str):
    """
        Convert a string to a x,y point
    """
    x, y = point_str.split(", ")
    return Point(int(x), int(y))

def get_manhattan_distance(point1: Point, point2: Point):
    """
        Get manhattan distance between two points
    """
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

def is_equidistant(source: Point, point2: Point, point3: Point) -> bool:
    """
        Is the distance between source and point2 the same as distance between source and point3
    """
    return get_manhattan_distance(source, point2) == get_manhattan_distance(source, point3)

def get_average_point(points: List[Point]) -> Point:
    """
        Get the average position of all the points
    """
    xes = [point.x for point in points]
    yes = [point.y for point in points]
    return Point(sum(xes) // len(xes), sum(yes) // len(yes))

def to_left(point: Point) -> Point:
    """
        Move the point left
    """
    return Point(point.x - 1, point.y)

def to_right(point: Point) -> Point:
    """
        Move the point right
    """
    return Point(point.x + 1, point.y)

def to_above(point: Point) -> Point:
    """
        Move the point above (Assuming 0,0 is top left)
    """
    return Point(point.x, point.y - 1)

def to_below(point: Point) -> Point:
    """
        Move the point down (Assuming 0,0 is top left)
    """
    return Point(point.x, point.y + 1)


class Grid(abc.Mapping):
    """
        A grid that you can set and get points from
    """

    def __init__(self, *, top, left, bottom, right, fill_function=lambda _: None):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        points = product(range(left, right + 1), range(top, bottom + 1))
        self.all_points_in_rectangle = {Point(x, y): fill_function(Point(x, y)) for x, y in points}

    def __iter__(self):
        return iter(self.all_points_in_rectangle)

    def __len__(self):
        return len(self.all_points_in_rectangle)

    def __getitem__(self, key: Point):
        return self.all_points_in_rectangle[key]

    def is_on_boundary(self, point: Point) -> bool:
        """
            Return if the point is on the boundary
        """
        return point.x in (self.left, self.right) or point.y in (self.top, self.bottom)

    def get_boundary_points(self) -> Iterable[Point]:
        """
            Get all the points on a boundary
        """
        return filter(self.is_on_boundary, self.all_points_in_rectangle)

    def __str__(self):
        """
            Print the string
        """
        output = ""
        for pos_y in range(self.top, self.bottom + 1):
            for pos_x in range(self.left, self.right + 1):
                output += "".join(self.all_points_in_rectangle[Point(pos_x, pos_y)])
            output += "\n"
        return output

def to_bounded_grid(points: List[Point], fill_func=lambda _: None) -> Grid:
    """
        Convert a set of point to a bounded grid
    """
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    return Grid(top=min(ys), bottom=max(ys), left=min(xs), right=max(xs), fill_function=fill_func)
