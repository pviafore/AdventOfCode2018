"""
    A module containing Points and Grids
"""
# we don't want to change x, y names because those are actually good names
# pylint: disable=invalid-name
from collections import abc, namedtuple
from itertools import product
from typing import Any, Callable, Iterable, List, Sequence, Tuple, Union

Point = namedtuple("Point", ["x", "y"])
NestedPoints = List[Tuple[Point, Any]]

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

def get_average_point(points: Sequence[Point]) -> Point:
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

class Grid(abc.MutableMapping):
    """
        A grid that you can set and get points from
    """

    def __init__(self, *, top, left, bottom, right, fill_function=lambda _: None):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.default_function = lambda: None
        points = product(range(left, right + 1), range(top, bottom + 1))
        self.all_points_in_rectangle = {Point(x, y): fill_function(Point(x, y)) for x, y in points}

    def __iter__(self):
        return iter(self.all_points_in_rectangle)

    def __len__(self):
        return len(self.all_points_in_rectangle)

    def __getitem__(self, key: Point):
        return self.all_points_in_rectangle[key]

    def __setitem__(self, key: Point, value):
        self.all_points_in_rectangle[key] = value

    def __delitem__(self, key: Point):
        self.all_points_in_rectangle = None

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


def to_bounded_grid(points: Sequence[Point], fill_func=lambda _: None) -> Grid:
    """
        Convert a set of point to a bounded grid
    """
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    return Grid(top=min(ys), bottom=max(ys), left=min(xs), right=max(xs), fill_function=fill_func)

def from_strings(text: Sequence[str], default=None) -> Grid:
    """
        From a row of strings create a grid
        If the point doesn't exist, fill with default
    """
    top = 0
    bottom = len(text)
    left = 0
    right = max(len(t) for t in text)

    def fill_function(point: Point):
        if point.y >= len(text) or point.x >= len(text[point.y]):
            return default
        return text[point.y][point.x]

    return Grid(top=top, bottom=bottom, left=left, right=right, fill_function=fill_function)

def get_orthogonally_adjacent(point: Point) -> List[Point]:
    """
        Get the 4 orthogonally adjacent points
    """
    return [to_above(point), to_left(point), to_right(point), to_below(point)]

class MapGrid(abc.MutableMapping):
    """
        A text grid that represents some sort of cartographical map
    """

    def __init__(self, text: Sequence[str], default: str):
        self.grid = from_strings(text, default)
        self.default = default

    def __str__(self):
        return str(self.grid)

    def get_characters(self, matcher: Union[str, Callable[[Point, Any], bool]]) -> NestedPoints:
        """
            Get all characters matching a point
        """
        matching_function = matcher if callable(matcher) else (lambda _p, x: x == matcher)
        return [(p, v) for p, v in self.grid.items() if matching_function(p, v)]

    def move(self, source: Point, destination: Point, backfill: str):
        """
            Move whatever token at source to destination, and backfill into source
        """
        self.grid[destination] = self.grid[source]
        self.grid[source] = backfill

    def __iter__(self):
        return iter(self.grid)

    def __len__(self):
        return len(self.grid)

    def __getitem__(self, key: Point):
        return self.grid[key]

    def __setitem__(self, key: Point, value):
        self.grid[key] = value

    def __delitem__(self, key: Point):
        self.grid[key] = self.default

    def is_valid(self, p: Point, invalid: Sequence[str]):
        """
            If the point is in the graph and not equal to invalid
        """
        return p in self.grid and self.grid[p] not in invalid

    def get_closest_targets(self, point: Point, targets: List[Point], obstacles: Sequence[str]):
        """
            Return a list of paths that are minimal distance to a target square
        """
        candidates = [(point, 0)]
        seen = set([point])
        while candidates:
            # See if any of our paths are targets
            valid_paths = [candidate for candidate in candidates if candidate[0] in targets]
            if valid_paths:
                return valid_paths

            new_paths = []
            for last, length in candidates:
                for orthogonal in get_orthogonally_adjacent(last):
                    if orthogonal not in seen and self.is_valid(orthogonal, obstacles):
                        new_path = (orthogonal, length + 1)
                        seen.add(orthogonal)
                        new_paths.append(new_path)

            candidates = new_paths

        return []


    def get_best_next_step(self, point: Point, target: Point, length: int, obstacles: str):
        """
            Get the best next step given a point and a target (and it has to be < length)
        """
        if point == target:
            return point
        orthogonal = [p for p in get_orthogonally_adjacent(point) if self.is_valid(p, obstacles)]
        paths = [(p, self.get_closest_targets(p, [target], obstacles)) for p in orthogonal]
        paths = [(first, answers[0]) for first, answers in paths if answers]
        return next(first for (first, (last, l)) in paths if l < length and last == target)

    def is_adjacent_to(self, point: Point, desired: str) -> bool:
        """
            Return true if the point is adjacent to a desired square
        """
        orthogonal = get_orthogonally_adjacent(point)
        return any(self.grid[p] == desired for p in orthogonal if self.is_valid(p, []))
