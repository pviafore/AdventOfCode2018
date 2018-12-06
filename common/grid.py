"""
    A module containing Points and Grids
"""
# we don't want to change x, y names because those are actually good names
# pylint: disable=invalid-name
from collections import abc, namedtuple
from itertools import product

Point = namedtuple("Point", ["x", "y"])

def to_point(point_str):
    """
        Convert a string to a x,y point
    """
    x, y = point_str.split(", ")
    return Point(int(x), int(y))

def get_manhattan_distance(point1, point2):
    """
        Get manhattan distance between two points
    """
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

def is_equidistant(source, point2, point3):
    """
        Is the distance between source and point2 the same as distance between source and point3
    """
    return get_manhattan_distance(source, point2) == get_manhattan_distance(source, point3)

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

    def __getitem__(self, key):
        return self.all_points_in_rectangle[key]

    def is_on_boundary(self, point):
        """
            Return if the point is on the boundary
        """
        return point.x in (self.left, self.right) or point.y in (self.top, self.bottom)

    def get_boundary_points(self):
        """
            Get all the points on a boundary
        """
        return filter(self.is_on_boundary, self.all_points_in_rectangle)

def to_bounded_grid(points, fill_func=lambda _: None):
    """
        Convert a set of point to a bounded grid
    """
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    return Grid(top=min(ys), bottom=max(ys), left=min(xs), right=max(xs), fill_function=fill_func)
