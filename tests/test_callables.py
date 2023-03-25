import froggytv.callables as callables
import pytest
from helpers.utils import FakeOutput, ImmediateBPM, is_even


class TestNoop:
    def test_noop_does_nothing(self):
        assert callables.Noop()(0) is None


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
        periodic = callables.Periodic(bpm.resolution, callable, mult=mult)

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
        periodic = callables.Periodic(bpm.resolution, callable, pwm=pwm)

        for _ in range(call_count):
            bpm.update(now, periodic)

        assert callable.on == expected_on
