from froggytv.triggers import Noop


def test_noop_does_nothing():
    assert Noop().trigger() is None
