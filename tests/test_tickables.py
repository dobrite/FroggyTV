import froggytv.tickables as tickables
from helpers.utils import CountingTickable, ImmediateBPM, FakeOutput
import pytest


class TestNoop:
    def test_noop_does_nothing(self):
        assert tickables.Noop().tick(0) is None


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
        division = tickables.Division(tickable, div)

        for _ in range(tick_count):
            bpm.update(now, division)

        assert tickable.count == expected_count


class TestTicksToTrigger:
    @pytest.fixture
    def triggerable(self):
        return FakeOutput()

    @pytest.mark.parametrize(
        "resolution, ticks_to_trigger, tick_count, expected_triggers",
        [
            (640, 10, 0, 0),
            (640, 10, 9, 1),
            (640, 10, 10, 1),
            (640, 10, 11, 2),
            (640, 32, 32, 1),
            (640, 32, 33, 2),
        ],
    )
    def test_ticks_to_trigger(
        self, triggerable, resolution, ticks_to_trigger, tick_count, expected_triggers
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        ticks_to_trigger = tickables.TicksToTrigger(ticks_to_trigger, triggerable)

        for _ in range(tick_count):
            bpm.update(now, ticks_to_trigger)

        assert triggerable.count == expected_triggers
