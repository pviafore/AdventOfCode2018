from challenge17 import WaterGrid
from common.grid import Grid, Point

def test_straight_flow():
    empty_grid = WaterGrid(Grid(top=0, left=0, bottom=2, right=2, fill_function=lambda _:"."))
    empty_grid.run_water(Point(1, -1))
    assert str(empty_grid) == ".|.\n.|.\n.|.\n"

def from_start(text):
    lines = text.split("\n")
    return WaterGrid(Grid(top=0, left=0, bottom=len(lines) - 1, right=len(lines[0]) - 1, fill_function=lambda p:lines[p.y][p.x]))

def test_hit_block():
    start = """...
.#.
..."""

    expected = """|||
|#|
|.|
"""

    grid = from_start(start)
    grid.run_water(Point(1, -1))
    assert str(grid) == expected

def test_hit_plane():
    start = """.....
.###.
....."""

    expected = """|||||
|###|
|...|
"""
    grid = from_start(start)
    grid.run_water(Point(2, -1))
    assert str(grid) == expected

def test_hit_plane_with_left_edge():
    start = """.#...
.###.
....."""

    expected = """.#|||
.###|
....|
"""
    grid = from_start(start)
    grid.run_water(Point(2, -1))
    assert str(grid) == expected

def test_hit_plane_with_right_edge():
    start = """....#
.###.
....."""

    expected = """||||#
|###.
|....
"""
    grid = from_start(start)
    grid.run_water(Point(2, -1))
    assert str(grid) == expected

def test_hit_deep_well():
    start = """......
.#..#.
.#..#.
.####."""

    expected = """||||||
|#~~#|
|#~~#|
|####|
"""
    grid = from_start(start)
    grid.run_water(Point(2, -1))
    assert str(grid) == expected

def test_hit_nested_block_with_drain():
    start = """.......
...#.#.
.#...#.
.#####."""

    expected = """..|||||
|||#~#|
|#~~~#|
|#####|
"""
    grid = from_start(start)
    grid.run_water(Point(3, -1))
    assert str(grid) == expected

def test_hit_nested_block_with_overflow():
    start = """.......
.#.#.#.
.#...#.
.#####."""

    expected = """|||||||
|#~#~#|
|#~~~#|
|#####|
"""
    grid = from_start(start)
    grid.run_water(Point(3, -1))
    assert str(grid) == expected

def test_hit_nested_block_at_bottom():
    start = """.......
.#...#.
.#.#.#.
.#####."""

    expected = """|||||||
|#~~~#|
|#~#~#|
|#####|
"""
    grid = from_start(start)
    grid.run_water(Point(3, -1))
    assert str(grid) == expected

def test_flows_in_both_directions():
    start = """........................
........................
........................
......................#.
.#....................#.
.#....................#.
.#....................#.
.######################."""

    expected = """...........|............
...........|............
...........|............
||||||||||||||||||||||#.
|#~~~~~~~~~~~~~~~~~~~~#.
|#~~~~~~~~~~~~~~~~~~~~#.
|#~~~~~~~~~~~~~~~~~~~~#.
|######################.
"""
    grid = from_start(start)
    grid.run_water(Point(11, -1))
    assert str(grid) == expected

def test_flows_dont_overlap():
    start = """........................
........###.............
........................
......................#.
.#....................#.
.#....................#.
.#....................#.
.######################."""

    expected = """.......|||||............
.......|###|............
.......|...|............
||||||||||||||||||||||#.
|#~~~~~~~~~~~~~~~~~~~~#.
|#~~~~~~~~~~~~~~~~~~~~#.
|#~~~~~~~~~~~~~~~~~~~~#.
|######################.
"""
    grid = from_start(start)
    grid.run_water(Point(10, -1))
    assert str(grid) == expected
