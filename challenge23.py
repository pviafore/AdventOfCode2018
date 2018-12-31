"""
    Advent of code Day 23
    Hoo boy this is ugly
"""
from collections import namedtuple
import heapq
from itertools import product
from re import split
from typing import List

from common.input_file import get_transformed_input
from common.grid import get_manhattan_distance

Nanobot = namedtuple("Nanobot", ["x", "y", "z", "radius"])

def to_nanobot(nanobot: str) -> Nanobot:
    """
        Convert a string to a nanobot
    """
    _, x_pos, y_pos, z_pos, radius = split(r"pos=<|,|>, r=", nanobot)
    return Nanobot(int(x_pos), int(y_pos), int(z_pos), int(radius))

def get_distance(bot1: Nanobot, bot2: Nanobot) -> int:
    """
        Get the distance between two nanobots
    """
    return get_manhattan_distance((bot1.x, bot1.y, bot1.z), (bot2.x, bot2.y, bot2.z))

def get_number_of_nanobots_within_strongest_range(nanobots) -> int:
    """
        Get number of nanobots within range of the strongest
    """
    strongest = max(nanobots, key=lambda n: n.radius)
    within_range = [n for n in nanobots if get_distance(strongest, n) < strongest.radius]
    return len(within_range)

def get_radius_resolution(nanobot: Nanobot, resolution: int):
    """
        Get the radius at the specified resolution
    """
    if nanobot.radius % resolution == 0:
        return nanobot.radius // resolution
    return (nanobot.radius // resolution) + 2

Cube = namedtuple("Cube", ["min_x", "min_y", "min_z", "max_x", "max_y", "max_z"])
def get_points(cube: Cube, nanobots: List[Nanobot], resolution: int):
    """
        Get a list of points and the nanobots that interesect each point
    """
    xes = range(cube.min_x // resolution, (cube.max_x // resolution))
    yes = range(cube.min_y // resolution, (cube.max_y // resolution))
    zes = range(cube.min_z // resolution, (cube.max_z // resolution))
    def is_within_range(bot, xpos, ypos, zpos):
        nanobot_point = (bot.x // resolution, bot.y // resolution, bot.z // resolution)
        distance = get_manhattan_distance(nanobot_point, (xpos, ypos, zpos))
        return distance <= get_radius_resolution(bot, resolution)
    for xpos, ypos, zpos in product(xes, yes, zes):
        yield (xpos, ypos, zpos), [n for n in nanobots if is_within_range(n, xpos, ypos, zpos)]

def get_initial_cube(nanobots) -> Cube:
    """
        Get the initial cube
    """
    xes = [n.x for n in nanobots]
    yes = [n.y for n in nanobots]
    zes = [n.z for n in nanobots]
    minx, maxx, miny, maxy, minz, maxz = min(xes), max(xes), min(yes), max(yes), min(zes), max(zes)
    return Cube(minx, miny, minz, maxx, maxy, maxz)

def get_initial_searchsquares(nanobots):
    """
        Get the initial set of search squares
    """
    cube = get_initial_cube(nanobots)
    initial_resolution = 100_000_000
    initial_points = get_points(cube, nanobots, initial_resolution)
    squares_to_check = []
    for point, bots in initial_points:
        distance = get_manhattan_distance(point, (0, 0, 0))
        searchsquare = (-len(bots), -initial_resolution, distance, point)
        heapq.heappush(squares_to_check, searchsquare)
    return squares_to_check

def get_next_points_from_cube(xpos, ypos, zpos, resolution, nanobots):
    """
        Get the next set of points from the cube
    """
    minx, miny, minz = xpos * resolution, ypos * resolution, zpos * resolution
    cube = Cube(minx, miny, minz, minx + resolution, miny + resolution, minz + resolution)
    return get_points(cube, nanobots, resolution // 10)

def get_most_intersections(nanobots):
    """
        Print out the interesections at each point (Doesn't return)
        Starts in 100_000_000 cubes and uses a priority queue to
        determine what cube to look at , dividing by 10 each time
    """
    squares_to_check = get_initial_searchsquares(nanobots)
    max_intersections = 0
    while squares_to_check:
        num_bots, resolution, __, (xpos, ypos, zpos) = heapq.heappop(squares_to_check)
        resolution *= -1
        num_bots *= -1
        if num_bots <= max_intersections:
            continue
        print(f"There are {num_bots} intersections at {(xpos, ypos, zpos)}: @ {resolution}")
        if resolution == 1:
            if num_bots > max_intersections:
                max_intersections = num_bots
        else:
            next_points = get_next_points_from_cube(xpos, ypos, zpos, resolution, nanobots)
            for next_point, next_bots in next_points:
                if len(next_bots) >= max_intersections:
                    distance = get_manhattan_distance((xpos, ypos, zpos), (0, 0, 0))
                    searchsquare = (-len(next_bots), -resolution // 10, distance, next_point)
                    heapq.heappush(squares_to_check, searchsquare)

NANOBOTS = get_transformed_input("input/input23.txt", to_nanobot)
print(get_number_of_nanobots_within_strongest_range(NANOBOTS))
print(get_most_intersections(NANOBOTS))
