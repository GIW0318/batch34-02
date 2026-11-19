import pytest

import procedural_cave as pc

ONE_ROOM = [
    "#######",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#######",
]

TWO_ROOMS = [
    "#######",
    "#..#..#",
    "#..#..#",
    "#..#..#",
    "#..#..#",
    "#..#..#",
    "#######",
]


def test_width_too_small_rejected():
    with pytest.raises(ValueError):
        pc.CaveMap(4, 10)


def test_height_too_small_rejected():
    with pytest.raises(ValueError):
        pc.CaveMap(10, 4)


def test_fill_above_one_rejected():
    with pytest.raises(ValueError):
        pc.CaveMap(10, 10, fill=1.2)


def test_fill_zero_rejected():
    with pytest.raises(ValueError):
        pc.CaveMap(10, 10, fill=0.0)


def test_negative_steps_rejected():
    cave = pc.CaveMap(10, 10)
    with pytest.raises(ValueError):
        cave.generate(steps=-1)


def test_invalid_birth_and_death_rejected():
    cave = pc.CaveMap(10, 10)
    with pytest.raises(ValueError):
        cave.generate(birth=4, death=4)


def test_generated_grid_has_requested_size():
    grid = pc.CaveMap(21, 21, seed=7).generate()
    assert len(grid) == 21
    assert all(len(row) == 21 for row in grid)


def test_generated_border_is_wall():
    grid = pc.CaveMap(21, 21, seed=7).generate()
    assert all(grid[0][x] == 1 for x in range(21))
    assert all(grid[20][x] == 1 for x in range(21))
    assert all(grid[y][0] == 1 for y in range(21))
    assert all(grid[y][20] == 1 for y in range(21))


def test_same_seed_is_deterministic():
    first = pc.CaveMap(21, 21, seed=7).generate()
    second = pc.CaveMap(21, 21, seed=7).generate()
    assert len(first) == 21
    assert first == second


def test_generated_grid_contains_floor_and_wall():
    grid = pc.CaveMap(21, 21, seed=7).generate()
    values = {cell for row in grid for cell in row}
    assert values <= {0, 1}
    assert 0 in values
    assert 1 in values


def test_single_room_is_connected():
    cave = pc.CaveMap.from_rows(ONE_ROOM)
    assert cave.connected() is True
    assert cave.components() == [25]


def test_two_rooms_are_not_connected():
    cave = pc.CaveMap.from_rows(TWO_ROOMS)
    assert cave.connected() is False
    assert cave.components() == [10, 10]


def test_repair_connects_components():
    cave = pc.CaveMap.from_rows(TWO_ROOMS)
    carved = cave.repair()
    assert carved > 0
    assert cave.connected() is True
    assert cave.repair() == 0
    grid = cave.state()["grid"]
    assert all(grid[0][x] == 1 for x in range(7))
    assert all(grid[6][x] == 1 for x in range(7))


def test_repair_on_connected_map_changes_nothing():
    cave = pc.CaveMap.from_rows(ONE_ROOM)
    assert cave.repair() == 0


def test_state_snapshot_is_independent():
    cave = pc.CaveMap.from_rows(TWO_ROOMS)
    snapshot = cave.state()
    assert snapshot["width"] == 7
    assert snapshot["height"] == 7
    snapshot["grid"][1][1] = 1
    assert cave.components() == [10, 10]
