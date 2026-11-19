import pytest

import navmesh_funnel as nf


def test_no_portals_returns_direct_segment():
    assert nf.funnel_path((0, 0), (6, 3), []) == [(0, 0), (6, 3)]


def test_straight_portal_adds_no_waypoint():
    portals = [((2, 1), (2, -1))]
    assert nf.funnel_path((0, 0), (4, 0), portals) == [(0, 0), (4, 0)]


def test_off_axis_portal_adds_no_waypoint():
    portals = [((2, 2), (2, 0))]
    assert nf.funnel_path((0, 0), (6, 3), portals) == [(0, 0), (6, 3)]


def test_jog_down_inserts_lower_waypoint():
    portals = [((4, 1), (4, -1)), ((8, -1), (8, -3))]
    assert nf.funnel_path((0, 0), (10, 0), portals) == [(0, 0), (8, -1), (10, 0)]


def test_jog_up_inserts_upper_waypoint():
    portals = [((4, 1), (4, -1)), ((8, 3), (8, 1))]
    assert nf.funnel_path((0, 0), (10, 0), portals) == [(0, 0), (8, 1), (10, 0)]


def test_degenerate_portal_becomes_waypoint():
    portals = [((4, 1), (4, -1)), ((8, -1), (8, -1))]
    assert nf.funnel_path((0, 0), (10, 0), portals) == [(0, 0), (8, -1), (10, 0)]


def test_right_angle_corner_pulls_string():
    portals = [((2, 1), (2, -1)), ((3, 2), (5, 2))]
    expected = [(0, 0), (2, 1), (3, 2), (4, 4)]
    assert nf.funnel_path((0, 0), (4, 4), portals) == expected


def test_s_shape_skips_unneeded_corners():
    portals = [((2, 1), (2, -1)), ((3, 2), (5, 2)), ((6, 5), (6, 3))]
    assert nf.funnel_path((0, 0), (8, 6), portals) == [(0, 0), (2, 1), (8, 6)]


def test_s_shape_keeps_forced_turn():
    portals = [((2, 1), (2, -1)), ((3, 2), (5, 2)), ((6, 3), (6, 5))]
    expected = [(0, 0), (2, 1), (6, 5), (8, 4)]
    assert nf.funnel_path((0, 0), (8, 4), portals) == expected


def test_same_start_and_goal_returns_single_point():
    assert nf.funnel_path((5, 5), (5, 5), []) == [(5, 5)]


def test_portals_none_is_rejected():
    with pytest.raises(ValueError):
        nf.funnel_path((0, 0), (4, 0), None)


def test_portal_must_be_a_pair_of_points():
    with pytest.raises(ValueError):
        nf.funnel_path((0, 0), (4, 0), [(2, 2)])


def test_three_dimensional_portal_is_rejected():
    with pytest.raises(ValueError):
        nf.funnel_path((0, 0), (4, 0), [((2, 0, 0), (2, 1, 0))])


def test_string_coordinate_is_rejected():
    with pytest.raises(ValueError):
        nf.funnel_path((0, 0), (4, 0), [((2, "1"), (2, 1))])


def test_three_dimensional_start_is_rejected():
    with pytest.raises(ValueError):
        nf.funnel_path((0, 0, 0), (4, 0), [])
