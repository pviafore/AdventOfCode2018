"""
    Day 25 of AoC
"""
from itertools import chain
from typing import List, Tuple

from common.grid import get_manhattan_distance
from common.input_file import get_transformed_input

Star = Tuple[int, int, int, int]
def to_4d_point(point_str: str):
    """
        Get a 4 dimensional point from the string
    """
    return tuple(map(int, point_str.split(",")))

def is_close(star: Star, constellation: List[Star]):
    """
        Return if a star is close enough to a constellation
    """
    return any(get_manhattan_distance(star, s) <= 3 for s in constellation)

def get_constellations(stars):
    """
        Get a list of constellations
    """
    constellations = []
    for star in stars:
        matching_constellations = [c for c in constellations if is_close(star, c)]
        constellations = [c for c in constellations if c not in matching_constellations]
        constellations.append(list(chain.from_iterable(matching_constellations)) + [star])
    return constellations

STARS = get_transformed_input("input/input25.txt", to_4d_point)
if __name__ == "__main__":
    print(len(get_constellations(STARS)))
