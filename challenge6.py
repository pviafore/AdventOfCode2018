from collections import Counter
from itertools import product
from common.input_file import get_transformed_input

def get_point(point_str):
    x,y = point_str.split(", ")
    return int(x), int(y)

def get_all_points(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    left, right, top, bottom = min(xs), max(xs), min(ys), max(ys)
    return product(range(left, right + 1), range(top, bottom + 1))
    
def is_point_region_infinite(point, points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    left, right, top, bottom = min(xs), max(xs), min(ys), max(ys)
    return point[0] in (left, right) or point[1] in (top, bottom) 


def get_manhattan_distance(point1, point2):
    (x1, y1), (x2, y2) = point1, point2
    return abs(x1 - x2) + abs(y1 - y2)

def get_largest_finite_region(points):
    total_grid = {}
    for p1 in get_all_points(points):
        closest_point = min((p2 for p2 in points), key=lambda p2: get_manhattan_distance(p1, p2))
        same_distance_points = [p2 for p2 in points if get_manhattan_distance(p1, p2) == get_manhattan_distance(p1, closest_point)]
        total_grid[p1] = closest_point if len(same_distance_points) == 1 else "."


    boundaries = [total_grid[p] for p in get_all_points(points) if total_grid[p] != "." and is_point_region_infinite(p, points)]
    ignored_elements = set(boundaries )
    c = Counter(closest for closest in total_grid.values() if closest != "." and closest not in ignored_elements)
    return c.most_common()[0][1]

def get_safest_finite_region(points):
    okay = []
    for p in get_all_points(points):
        distance = sum(get_manhattan_distance(p, p2) for p2 in points)
        if distance < 10000:
            okay.append(p)
    return len(okay)

POINTS = get_transformed_input("input/input6.txt", get_point)
if __name__ == "__main__":
    print(get_largest_finite_region(POINTS))
    print(get_safest_finite_region(POINTS))