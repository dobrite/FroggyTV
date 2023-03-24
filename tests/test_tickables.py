from froggytv.tickables import Noop


class TestNoop:
    def test_noop_does_nothing(self):
        assert Noop().tick(0) is None
