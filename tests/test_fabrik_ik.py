import math

import pytest

import fabrik_ik as fk


def chain():
    return fk.FabrikChain([2.0, 3.0], base=(0.0, 0.0))


def gap(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def test_empty_lengths_rejected():
    with pytest.raises(ValueError):
        fk.FabrikChain([], base=(0.0, 0.0))


def test_zero_length_rejected():
    with pytest.raises(ValueError):
        fk.FabrikChain([2.0, 0.0], base=(0.0, 0.0))


def test_negative_length_rejected():
    with pytest.raises(ValueError):
        fk.FabrikChain([2.0, -1.0], base=(0.0, 0.0))


def test_base_must_be_two_dimensional():
    with pytest.raises(ValueError):
        fk.FabrikChain([1.0, 1.0], base=(0.0, 0.0, 0.0))


def test_tolerance_must_be_positive():
    with pytest.raises(ValueError):
        chain().solve((2.0, 3.0), tolerance=0.0)


def test_iteration_cap_must_be_positive():
    with pytest.raises(ValueError):
        chain().solve((2.0, 3.0), max_iterations=0)


def test_target_dimension_mismatch():
    with pytest.raises(ValueError):
        chain().solve((2.0, 3.0, 0.0))


def test_target_equal_to_base_rejected():
    with pytest.raises(ValueError):
        chain().solve((0.0, 0.0))


def test_reach_is_sum_of_lengths():
    assert chain().reach == pytest.approx(5.0)


def test_reachable_target_is_hit():
    points = chain().solve((2.0, 3.0))
    assert gap(points[-1], (2.0, 3.0)) <= 1e-6


def test_base_stays_fixed_and_point_count():
    points = chain().solve((2.0, 3.0))
    assert len(points) == 3
    assert points[0] == (0.0, 0.0)


def test_segment_lengths_are_preserved():
    points = chain().solve((3.0, 2.0))
    lengths = [gap(points[i], points[i + 1]) for i in range(2)]
    assert lengths[0] == pytest.approx(2.0, abs=1e-6)
    assert lengths[1] == pytest.approx(3.0, abs=1e-6)


def test_unreachable_target_stretches_straight():
    points = chain().solve((10.0, 0.0))
    assert gap(points[-1], (5.0, 0.0)) <= 1e-6
    assert gap(points[1], (2.0, 0.0)) <= 1e-6
    assert all(abs(point[1]) <= 1e-6 for point in points)


def test_iteration_cap_is_respected():
    arm = chain()
    points = arm.solve((3.0, 2.0), max_iterations=1)
    assert arm.last_iterations == 1
    assert gap(points[-1], (3.0, 2.0)) > 1e-3
    lengths = [gap(points[i], points[i + 1]) for i in range(2)]
    assert lengths[0] == pytest.approx(2.0, abs=1e-6)
    assert lengths[1] == pytest.approx(3.0, abs=1e-6)


def test_repeated_solves_are_identical():
    arm = chain()
    first = arm.solve((3.0, 2.0))
    second = arm.solve((3.0, 2.0))
    assert len(first) == 3
    assert first == second
