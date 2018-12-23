"""
    Day 17 Advent of code
"""
from itertools import chain, product
from typing import Callable, List, Iterable

from common.grid import Point, Grid, to_bounded_grid, to_below, to_above, to_left, to_right
from common.input_file import get_transformed_input
PointMover = Callable[[Point], Point]
def to_points(points_str: str) -> List[Point]:
    """
        Given a string, convert it into a list of points
    """
    coord1, coord2 = points_str.split(", ")
    x_points, y_points = (coord2, coord1) if coord1.startswith("y") else (coord1, coord2)
    x_points, y_points = x_points.lstrip("x="), y_points.lstrip("y=")
    points = [Point(x, y) for x, y in product(parse_range(x_points), parse_range(y_points))]
    return points

def parse_range(range_str: str) -> Iterable[int]:
    """
        Parse a range (if there is a .. do an inclusive range)
    """
    if ".." in range_str:
        min_num, max_num = range_str.split("..")
        return range(int(min_num), int(max_num) + 1)
    return [int(range_str)]


class WaterGrid:
    """
        A grid that maps water flow
    """
    def __init__(self, grid: Grid):
        self.grid = grid

    def flow(self, point: Point):
        """
            Flow water into the square
        """
        assert self.grid[point] not in "#~", f"{self.grid} {point}"
        self.grid[point] = "|"

    def rest(self, point: Point):
        """
            Rest water at point
        """
        assert self.grid[point] not in "#"
        self.grid[point] = "~"

    def __str__(self):
        return str(self.grid)

    def contains(self, point: Point) -> bool:
        """
            If the water grid contains the point
        """
        return point in self.grid

    def is_solid(self, point: Point) -> bool:
        """
            Check if the point is solid
        """
        return self.grid.get(point, ".") == "#"

    def is_water(self, point: Point) -> bool:
        """
            Check if the point is solid
        """
        return self.grid.get(point, ".") == "~"

    def is_empty(self, point: Point) -> bool:
        """
            Check if a point is water
        """
        return self.grid.get(point, ".") == "."

    def is_flowing(self, point: Point) -> bool:
        """
            Check if a point is flowing
        """
        return self.grid.get(point, ".") == "|"

    def can_drip(self, point: Point) -> bool:
        """
            Returns if the water can drip below point
        """
        return not self.is_solid(to_below(point)) and not self.is_water(to_below(point))

    def spread_horizontal(self, source: Point, direction: PointMover) -> Point:
        """
            Spread horizontally as far as you can
            Return the point that we need to stop
        """
        bound = source
        while not self.can_drip(bound) and self.is_empty(direction(bound)):
            bound = self.flow_horizontal(bound, direction)
            if self.can_drip(bound):
                self.run_water(bound)
        return bound

    def run_water(self, source: Point):
        """
            Run water through the grid
        """
        original = source
        source = to_below(source)
        while source != original and self.contains(source):
            self.flow(source)
            next_block = to_below(source)
            if self.is_flowing(next_block):
                break
            if self.is_solid(next_block) or self.is_water(next_block):
                left_bound = self.spread_horizontal(source, to_left)
                right_bound = self.spread_horizontal(source, to_right)

                if not self.can_drip(right_bound) and not self.can_drip(left_bound):
                    self.fill(left_bound, right_bound)
                    next_block = to_above(source)
                else:
                    break

            source = next_block

    def flow_horizontal(self, source: Point, direction_func: PointMover) -> Point:
        """
           Flow water horizontally
        """
        while not self.is_solid(direction_func(source)) and not self.can_drip(source):
            source = direction_func(source)
            self.flow(source)
        return source

    def fill(self, left_bound: Point, right_bound: Point):
        """
            Fill from left to right bound wiht ~
        """
        while left_bound != right_bound:
            self.rest(left_bound)
            left_bound = to_right(left_bound)
        self.rest(right_bound)

    def get_number_of_tiles_water_reached(self) -> int:
        """
            Get the number of tiles that water reached
        """
        return len([p for p in self.grid if self.grid[p] in "~|"])

    def get_number_of_tiles_at_rest(self) -> int:
        """
            Get the number of tiles with water at rest
        """
        return len([p for p in self.grid if self.grid[p] == "~"])


def create_grid() -> WaterGrid:
    """
        Read a file and give al ist of points
    """
    points = set(chain.from_iterable(get_transformed_input("input/input17.txt", to_points)))

    def fill_function(point):
        return "#" if point in points else "."

    grid = WaterGrid(to_bounded_grid(points, fill_function, padding=(1, 0)))
    grid.run_water(Point(500, grid.grid.top -1))
    return grid

GRID = create_grid()
if __name__ == "__main__":
    print(GRID.get_number_of_tiles_water_reached())
    print(GRID.get_number_of_tiles_at_rest())
