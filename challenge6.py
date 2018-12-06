"""
    Advent of code Day 6
"""
from collections import Counter
from common.grid import to_bounded_grid, to_point, is_equidistant, get_manhattan_distance
from common.input_file import get_transformed_input

TIED = "."

def get_closest_point(point, points):
    """
        Get Closest point to the current point or "." if tied
    """
    closest_point = min(points, key=lambda p: get_manhattan_distance(p, point))
    closest_points = [p for p in points if is_equidistant(point, p, closest_point)]
    return closest_point if len(closest_points) == 1 else TIED

def get_largest_finite_region(points):
    """
        Get the largest finite region
    """
    grid = to_bounded_grid(points, lambda point: get_closest_point(point, points))
    boundaries = set(grid[p] for p in grid.get_boundary_points() if grid[p] != TIED)
    counter = Counter(closest for closest in grid.values() if closest not in boundaries)
    return counter.most_common(0)[0][1]

def get_safest_finite_region(points):
    """
        Get the safest finite region
    """
    grid = to_bounded_grid(points)
    distances = (get_summed_distance(p, points) for p in grid)
    return len([d for d in distances if d < 10000])

def get_summed_distance(point, points):
    """
        Return a summed manhattan distance from this point to all other points)
    """
    return sum(get_manhattan_distance(p, point) for p in points)

POINTS = get_transformed_input("input/input6.txt", to_point)
if __name__ == "__main__":
    print(get_largest_finite_region(POINTS))
    print(get_safest_finite_region(POINTS))
