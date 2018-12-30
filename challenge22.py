"""
    Day 22 of Advent of Code 2018
"""
import heapq
from typing import Set, List, Tuple
from common.grid import to_bounded_grid, Point, to_above, to_left, get_orthogonally_adjacent

class Cave:
    """
        A cave to explore for Rudolph
    """

    def __init__(self, target: Point, depth: int):
        self.target = target
        self.depth = depth
        self.grid = to_bounded_grid([Point(0, 0), self.target])
        for point in self.grid:
            self.grid[point] = self.get_geologic_level(point)

    def get_geologic_level(self, point: Point) -> int:
        """
            Get the geologic level of a point
        """
        if point == self.target:
            return 0
        if point.y == 0:
            return point.x * 16807
        if point.x == 0:
            return point.y * 48271
        return self.get_erosion_level(to_above(point)) * self.get_erosion_level(to_left(point))

    def get_erosion_level(self, point: Point) -> int:
        """
            Get the erosion level of from the geologic level
        """
        return (self.grid[point] + self.depth) % 20183

    def get_region(self, point: Point) -> int:
        """
            Get the region type based on erosion level
        """
        return self.get_erosion_level(point) % 3

    def get_total_risk_level(self) -> int:
        """
            Return the total risk level
        """
        origin = Point(0, 0)
        bounded_points = self.grid.get_bounded_points(origin, self.target)
        return sum(self.get_region(point) for point, _ in bounded_points)

    def can_traverse(self, equipment: str, point: Point) -> bool:
        """
            Return if we can traverse to the next point
        """
        region_type = self.get_region(point)
        traversable = [
            ["torch", "climbing"],
            ["climbing", "neither"],
            ["torch", "neither"]
        ]
        return equipment in traversable[region_type]

    def grow_if_needed(self, points: List[Point]):
        """
            Grow the grid down and to the right
        """
        if any(p not in self.grid for p in points):
            right = self.grid.right + 1
            bottom = self.grid.bottom + 1
            for y_pos in range(self.grid.top, bottom):
                new_point = Point(right, y_pos)
                self.grid[new_point] = self.get_geologic_level(new_point)
            for x_pos in range(self.grid.left, right + 1):
                new_point = Point(x_pos, bottom)
                self.grid[new_point] = self.get_geologic_level(new_point)


Move = Tuple[int, Point, str]
def get_toolchanges(move: Move, cave: Cave) -> List[Move]:
    """
        Get a list of toolchanges
    """
    distance, point, equipment = move
    tools = [t for t in ["torch", "climbing", "neither"] if t != equipment]
    return [(distance+7, point, e) for e in tools if cave.can_traverse(e, point)]

def get_adjacent_moves(move: Move, cave: Cave) -> List[Move]:
    """
        Get the adjacent moves
        Will grow the grid if necessary
    """
    distance, point, equip = move
    moves = [p for p in get_orthogonally_adjacent(point) if p.x >= 0 and p.y >= 0]
    in_grid = [m for m in moves if m.x >= 0 and m.y >= 0]
    cave.grow_if_needed(in_grid)
    return [(distance+1, m, equip) for m in in_grid if cave.can_traverse(equip, m)]


def get_fewest_minutes(cave: Cave) -> int:
    """
        Get the fewest minutes until the target
    """
    origin = Point(0, 0)
    seen: Set[Tuple[Point, str]] = set()
    nodes = [(0, origin, "torch")]
    min_distance = (cave.target.x + cave.target.y) * 8
    while nodes:
        move = heapq.heappop(nodes)
        if (move[1], move[2]) in seen:
            continue
        if move[1] == cave.target and move[2] == "torch":
            min_distance = min(min_distance, move[0])
        seen.add((move[1], move[2]))
        next_moves = get_toolchanges(move, cave) + get_adjacent_moves(move, cave)
        next_moves = [m for m in next_moves if m[0] < min_distance and (m[1], m[2]) not in seen]
        for new_move in next_moves:
            heapq.heappush(nodes, new_move)
    return min_distance

TARGET = Point(15, 740)
DEPTH = 3558
CAVE = Cave(TARGET, DEPTH)

if __name__ == "__main__":
    print(CAVE.get_total_risk_level())
    print(get_fewest_minutes(CAVE))
