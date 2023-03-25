from froggytv.tickables import Division, Noop, FanOut
from helpers.utils import CountingTickable, ImmediateBPM
import pytest


class TestNoop:
    def test_noop_does_nothing(self):
        assert Noop().tick(0) is None


class TestDivision:
    @pytest.fixture
    def tickable(self):
        return CountingTickable()

    @pytest.mark.parametrize(
        "resolution, div, tick_count, expected_count",
        [
            (640, 1, 0, 0),
            (640, 1, 1, 1),
            (640, 1, 640, 640),
            (640, 10, 640, 64),
            (640, 10, 6400, 640),
        ],
    )
    def test_division(self, tickable, resolution, div, tick_count, expected_count):
        now = None
        bpm = ImmediateBPM(resolution)
        division = Division(tickable, div)
        fan_out = FanOut([division])

        for _ in range(tick_count):
            bpm.update(now, fan_out)

        assert tickable.count == expected_count
