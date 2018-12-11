"""
    Advent of Code day 10
"""

from collections import namedtuple
from itertools import count
import re

from common.grid import Point, Grid, get_manhattan_distance, get_average_point
from common.input_file import get_transformed_input

def to_star(star_str):
    """
        Takes a star string and converts it to a star
    """
    regex = r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s* (-?\d+)>"
    match = re.match(regex, star_str)
    position = Point(int(match.group(1)), int(match.group(2)))
    return Star(position, int(match.group(3)), int(match.group(4)))
Star = namedtuple("Star", ["position", "velocity_x", "velocity_y"])

def move_star(star):
    """
        Move the star to the next location
    """
    new_position = Point(star.position.x + star.velocity_x, star.position.y + star.velocity_y)
    return Star(new_position, star.velocity_x, star.velocity_y)


def starfill(positions, point):
    """
        Return a # if its a star, otherwise blank space
    """
    return "#" if point in positions else " "

def draw_grid_and_counter(starpos, positions, counter):
    """
        Draw the grid given centered on starpos
    """
    grid_params = {
        "top": starpos.y - 20,
        "bottom": starpos.y + 20,
        "left": starpos.x - 100,
        "right": starpos.x + 100,
        "fill_function": lambda point: starfill(positions, point)
    }
    bounded_grid = Grid(**grid_params)
    print(bounded_grid)

    print("*"* 80)
    print(counter)
    print("*"* 80)

def run_animation(stars):
    """
        Run the animation loop
    """
    for counter in count():
        positions = [star.position for star in stars]
        average_position = get_average_point(positions)
        if get_manhattan_distance(stars[0].position, average_position) < 1000:
            draw_grid_and_counter(stars[0].position, positions, counter)
        stars = [move_star(star) for star in stars]

STARS = get_transformed_input("input/input10.txt", to_star)
if __name__ == "__main__":
    run_animation(STARS)
