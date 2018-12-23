"""
    Day 18 Advent of Code 2018
"""
from typing import Dict, Sequence

from common.input_file import read_strings
from common.grid import TextGrid, Point

OPEN = "."
LUMBERYARD = "#"
TREE = "|"


def transform(acre: str, surrounding: Sequence[str]) -> str:
    """
        Transform an acre based on its surroundings
    """
    if acre == OPEN and surrounding.count(TREE) >= 3:
        return TREE
    if acre == TREE and surrounding.count(LUMBERYARD) >= 3:
        return LUMBERYARD
    if acre == LUMBERYARD:
        if surrounding.count(LUMBERYARD) >= 1 and surrounding.count(TREE) >= 1:
            return LUMBERYARD
        return OPEN
    return acre

def get_surrounding(grid: TextGrid, point: Point) -> Sequence[str]:
    """
        Get the surrounding characters
    """
    return [acre for _, acre in grid.get_surrounding(point)]

def transform_grid(grid: TextGrid):
    """
        transform the grid through one iteration
    """
    values = [(p, transform(acre, get_surrounding(grid, p))) for p, acre in grid.items()]
    for point, acre in values:
        grid[point] = acre

def transform_over_time(grid: TextGrid, iterations: int):
    """
        Transform the grid a bunch of times
    """
    seen: Dict[str, int] = {}
    for iteration in range(iterations):
        transform_grid(grid)
        if str(grid) in seen:

            last_seen = seen[str(grid)]
            cycle_length = iteration - last_seen
            while iteration + cycle_length < iterations:
                iteration += cycle_length
            while iteration != iterations - 1:
                iteration += 1
                transform_grid(grid)
            break
        seen[str(grid)] = iteration

def get_total_resource_value(grid: TextGrid) -> int:
    """
        Get the total resource value
    """
    return len(grid.get_characters(TREE)) * len(grid.get_characters(LUMBERYARD))


GRID = TextGrid(read_strings("input/input18.txt"), default=".")
if __name__ == "__main__":
    transform_over_time(GRID, 10)
    print(get_total_resource_value(GRID))

    GRID = TextGrid(read_strings("input/input18.txt"), default=".")
    transform_over_time(GRID, 1_000_000_000)
    print(get_total_resource_value(GRID))
