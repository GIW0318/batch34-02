import pytest

import quadtree_broadphase as qb


def tree(capacity=2, max_depth=4):
    return qb.QuadtreeBroadphase((0, 0, 16, 16), capacity=capacity, max_depth=max_depth)


def test_bounds_width_must_be_positive():
    with pytest.raises(ValueError):
        qb.QuadtreeBroadphase((0, 0, 0, 16))


def test_capacity_must_be_positive():
    with pytest.raises(ValueError):
        qb.QuadtreeBroadphase((0, 0, 16, 16), capacity=0)


def test_max_depth_must_not_be_negative():
    with pytest.raises(ValueError):
        qb.QuadtreeBroadphase((0, 0, 16, 16), max_depth=-1)


def test_insert_then_query_returns_id():
    t = tree()
    t.insert("a", (1, 1, 4, 4))
    assert t.query((0, 0, 6, 6)) == ["a"]


def test_duplicate_id_is_rejected():
    t = tree()
    t.insert("a", (1, 1, 4, 4))
    with pytest.raises(ValueError):
        t.insert("a", (8, 8, 2, 2))


def test_rect_outside_bounds_is_rejected():
    t = tree()
    with pytest.raises(ValueError):
        t.insert("a", (14, 14, 4, 4))


def test_rect_size_must_be_positive():
    t = tree()
    with pytest.raises(ValueError):
        t.insert("a", (1, 1, 0, 2))


def test_query_returns_sorted_ids():
    t = tree()
    t.insert("z", (8, 8, 2, 2))
    t.insert("a", (0, 0, 2, 2))
    t.insert("m", (4, 4, 2, 2))
    assert t.query((0, 0, 16, 16)) == ["a", "m", "z"]


def test_remove_existing_returns_true():
    t = tree()
    t.insert("a", (1, 1, 4, 4))
    assert t.remove("a") is True
    assert t.query((0, 0, 16, 16)) == []


def test_remove_unknown_returns_false():
    assert tree().remove("missing") is False


def test_update_moves_object():
    t = tree()
    t.insert("a", (0, 0, 2, 2))
    t.update("a", (10, 10, 2, 2))
    assert t.query((0, 0, 4, 4)) == []
    assert t.query((9, 9, 4, 4)) == ["a"]


def test_pairs_find_overlap_across_quadrant():
    t = tree()
    t.insert("a", (1, 1, 3, 3))
    t.insert("b", (3, 3, 3, 3))
    assert t.pairs() == [("a", "b")]


def test_pairs_order_is_deterministic():
    rects = [("a", (1, 1, 3, 3)), ("b", (2, 2, 3, 3)), ("c", (3, 3, 3, 3))]
    first = tree()
    for name, rect in rects:
        first.insert(name, rect)
    second = tree()
    for name, rect in reversed(rects):
        second.insert(name, rect)
    expected = [("a", "b"), ("a", "c"), ("b", "c")]
    assert first.pairs() == expected
    assert second.pairs() == expected


def test_pairs_skip_separated_objects():
    t = tree()
    t.insert("a", (0, 0, 2, 2))
    t.insert("b", (10, 10, 2, 2))
    assert t.pairs() == []


def test_state_snapshot_is_independent():
    t = tree()
    t.insert("a", (1, 1, 4, 4))
    snapshot = t.state()
    assert snapshot["count"] == 1
    snapshot["items"]["a"] = (9, 9, 1, 1)
    assert t.query((0, 0, 6, 6)) == ["a"]
