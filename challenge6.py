from collections import abc, Counter, namedtuple
from itertools import product
from common.input_file import get_transformed_input

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_manhattan_distance(self, point):
        return abs(self.x - point.x) + abs(self.y - point.y)


def to_point(point_str):
    x, y = point_str.split(", ")
    return Point(x, y)

class Grid(abc.Iterable):

    def __init__(self, *, top, left, bottom, right ):
        points = product(range(left, right + 1), range(top, bottom + 1)) 
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.all_points_in_rectangle = Point(x,y) for x,y in points)

    def __iter__(self):
        return self.all_points_in_rectangle

def to_bounded_grid(points):
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    return Grid(top=min(ys), bottom=max(ys), left=min(xs), right=max(xs))
    top, bottom, left, right

def get_largest_finite_region(points):
    total_grid = {}
    for p1 in to_bounded_grid(points): 
        closest_point = min(points, key=p1.get_manhattan_distance)
        same_distance_points = [p2 for p2 in points if p1.get_manhattan_distance(p2) == p1.get_manhattan_distance(closest_point)]
        total_grid[p1] = closest_point if len(same_distance_points) == 1 else "."


    boundaries = set(total_grid[p] for p in grid if total_grid[p] != "." and is_point_region_infinite(p, points))
    c = Counter(closest for closest in total_grid.values() if closest != "." and closest not in ignored_elements)
    return c.most_common()[0][1]

def get_safest_finite_region(points):
    okay = []
    for p in to_bounded_grid(points):
        distance = sum(map(p.get_manhattan_distance, points))
        if distance < 10000:
            okay.append(p)
    return len(okay)

POINTS = get_transformed_input("input/input6.txt", to_point)
if __name__ == "__main__":
    print(get_largest_finite_region(POINTS))
    print(get_safest_finite_region(POINTS))