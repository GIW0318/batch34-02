import pytest

import flow_field as ff


def open_field():
    field = ff.FlowField(3, 3)
    field.set_goal((0, 0))
    field.compute()
    return field


def wall_field():
    blocked = {(2, 0), (2, 1), (2, 2), (2, 3)}
    field = ff.FlowField(5, 5, blocked=blocked)
    field.set_goal((4, 2))
    field.compute()
    return field


def test_width_must_be_positive():
    with pytest.raises(ValueError):
        ff.FlowField(0, 3)


def test_height_must_be_positive():
    with pytest.raises(ValueError):
        ff.FlowField(3, 0)


def test_blocked_cells_must_be_inside_grid():
    with pytest.raises(ValueError):
        ff.FlowField(3, 3, blocked={(5, 5)})


def test_goal_outside_grid_rejected():
    field = ff.FlowField(3, 3)
    with pytest.raises(ValueError):
        field.set_goal((3, 0))


def test_goal_on_blocked_cell_rejected():
    field = ff.FlowField(3, 3, blocked={(1, 1)})
    with pytest.raises(ValueError):
        field.set_goal((1, 1))


def test_goal_distance_is_zero():
    assert open_field().distance(0, 0) == 0


def test_adjacent_distance_is_one():
    assert open_field().distance(1, 0) == 1


def test_open_grid_uses_manhattan_distance():
    assert open_field().distance(2, 2) == 4


def test_direction_points_toward_goal():
    assert open_field().direction(2, 0) == (-1, 0)


def test_goal_direction_is_zero():
    assert open_field().direction(0, 0) == (0, 0)


def test_blocked_cell_direction_is_zero():
    field = ff.FlowField(3, 3, blocked={(1, 1)})
    field.set_goal((2, 2))
    field.compute()
    assert field.direction(1, 1) == (0, 0)


def test_tie_break_prefers_smaller_row():
    assert open_field().direction(2, 2) == (0, -1)


def test_wall_forces_detour():
    field = wall_field()
    expected = [(0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (3, 3), (3, 2), (4, 2)]
    assert field.distance(0, 2) == 8
    assert field.path((0, 2)) == expected


def test_expensive_cell_is_avoided():
    field = ff.FlowField(3, 3, costs={(1, 1): 9})
    field.set_goal((2, 2))
    field.compute()
    route = field.path((0, 0))
    assert (1, 1) not in route
    assert route == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    assert field.distance(0, 0) == 4


def test_unreachable_start_returns_empty_path():
    field = ff.FlowField(3, 3, blocked={(1, 0), (1, 1), (1, 2)})
    field.set_goal((2, 2))
    field.compute()
    assert field.path((0, 0)) == []
    assert field.distance(0, 0) is None
