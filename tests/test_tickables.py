import froggytv.tickables as tickables
from helpers.utils import CountingTickable, ImmediateBPM, FakeOutput, is_even
import pytest


class TestNoop:
    def test_ticking_noop_does_nothing(self):
        assert tickables.Noop().tick(0) is None

    def test_calling_noop_does_nothing(self):
        assert tickables.Noop()(0) is None


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


class TestTicksToCall:
    @pytest.fixture
    def callable(self):
        return FakeOutput()

    @pytest.mark.parametrize(
        "resolution, ticks_to_call, tick_count, expected_calls",
        [
            (640, 10, 0, 0),
            (640, 10, 9, 1),
            (640, 10, 10, 1),
            (640, 10, 11, 2),
            (640, 32, 32, 1),
            (640, 32, 33, 2),
        ],
    )
    def test_ticks_to_call(
        self, callable, resolution, ticks_to_call, tick_count, expected_calls
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        ticks_to_call = tickables.TicksToCall(ticks_to_call, callable)

        for _ in range(tick_count):
            bpm.update(now, ticks_to_call)

        assert callable.count == expected_calls


class TestPeriodic:
    @pytest.fixture
    def callable(self):
        return FakeOutput()

    @pytest.mark.parametrize(
        "resolution, mult, call_count, expected_count",
        [
            (640, 1, 0, 0),
            (640, 1, 1, 1),
            (640, 1, 640, 2),
            (640, 1, 641, 3),
            (640, 2, 640, 4),
            (640, 2, 641, 5),
            (640, 2, 960, 6),
            (640, 2, 961, 7),
            (640, 0.5, 1280, 2),
            (640, 0.5, 1281, 3),
        ],
    )
    def test_periodic(
        self,
        callable,
        resolution,
        mult,
        call_count,
        expected_count,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        periodic = tickables.Periodic(bpm.resolution, callable, mult=mult)

        for _ in range(call_count):
            bpm.update(now, periodic)

        assert callable.count == expected_count
        assert callable.on == is_even(expected_count)

    @pytest.mark.parametrize(
        "resolution, pwm, call_count, expected_on",
        [
            (640, 0.5, 0, False),
            (640, 0.5, 1, True),
            (640, 0.5, 320, True),
            (640, 0.5, 321, False),
            (640, 0.5, 640, False),
            (640, 0.5, 641, True),
        ],
    )
    def test_pwm(
        self,
        callable,
        resolution,
        pwm,
        call_count,
        expected_on,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        periodic = tickables.Periodic(bpm.resolution, callable, pwm=pwm)

        for _ in range(call_count):
            bpm.update(now, periodic)

        assert callable.on == expected_on
