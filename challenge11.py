"""
    Advent of code Day 11 (It's ugly)
"""

from itertools import product, chain
from common.grid import Grid, Point

SERIAL_NUMBER = 6303

def to_power_level(point):
    """
        Get the power level at a point
    """
    rack_id = point.x + 10
    power_level = rack_id * point.y + SERIAL_NUMBER
    power_level *= rack_id
    power_level = get_hundreds_digit(power_level)
    return power_level - 5

def get_hundreds_digit(power_level):
    """
        Get the hundreds digit
    """
    return 0 if power_level < 100 else int(str(power_level)[-3])


def get_power_levels(grid, square=3):
    """
        Get the power levels of each square of a certain size (defaults to 3)
    """
    initial = range(1, square+1)
    power_level = sum(grid[Point(x, y)] for x, y in product(initial, initial))
    yield (1, 1), power_level
    for y_pos in range(grid.top + 1, grid.bottom - square):
        power_level += sum(grid[Point(x, y_pos+square-1)] for x in initial)
        power_level -= sum(grid[Point(x, y_pos-1)] for x in initial)
        yield (1, y_pos, square), power_level

    power_level = sum(grid[Point(x, y)] for x, y in product(initial, initial))
    for x_pos in range(grid.left + 1, grid.right - square):
        power_level += sum(grid[Point(x_pos + square-1, y)] for y in initial)
        power_level -= sum(grid[Point(x_pos - 1, y)] for y in initial)
        yield (x_pos, 1, square), power_level

        y_power_level = power_level
        for y_pos in range(grid.top + 1, grid.bottom - square):
            y_power_level += sum(grid[Point(x, y_pos + square - 1)] for x in range(x_pos, x_pos+square))
            y_power_level -= sum(grid[Point(x, y_pos - 1)] for x in range(x_pos, x_pos+square))
            yield (x_pos, y_pos, square), y_power_level

def get_all_power_levels(grid):
    """
        Get all power levels (for every square size)
    """
    yield from chain.from_iterable(get_power_levels(grid, s) for s in range(1, 301))

GRID = Grid(top=1, left=1, bottom=300, right=300, fill_function=to_power_level)
print(max(get_power_levels(GRID), key=lambda t: t[1]))
print(max(get_all_power_levels(GRID), key=lambda t: t[1]))
