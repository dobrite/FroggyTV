from froggytv.triggers import Periodic, Division, Noop, Counter
from helpers.utils import ImmediateBPM, is_even
import pytest


class TestNoop:
    def test_ticking_noop_does_nothing(self):
        assert Noop().tick(0) is None

    def test_calling_noop_does_nothing(self):
        assert Noop()(0) is None


class TestDivision:
    @pytest.mark.parametrize(
        "resolution, div, tick_call_count, expected_count",
        [
            (640, 1, 0, 0),
            (640, 1, 1, 1),
            (640, 1, 640, 640),
            (640, 10, 640, 64),
            (640, 10, 6400, 640),
        ],
    )
    def test_division(
        self, test_output, resolution, div, tick_call_count, expected_count
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        division = Division(test_output, div)

        for _ in range(tick_call_count):
            bpm.update(now, division)

        assert test_output.tick_call_count == expected_count


class TestCounter:
    @pytest.mark.parametrize(
        "resolution, trigger_count, tick_call_count, expected_calls",
        [
            (640, 10, 0, 0),
            (640, 10, 1, 1),
            (640, 10, 9, 1),
            (640, 10, 10, 1),
            (640, 10, 11, 2),
            (640, 32, 32, 1),
            (640, 32, 33, 2),
        ],
    )
    def test_counter(
        self, test_output, resolution, trigger_count, tick_call_count, expected_calls
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        counter = Counter(trigger_count, test_output)

        for _ in range(tick_call_count):
            bpm.update(now, counter)

        assert test_output.call_count == expected_calls


class TestPeriodic:
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
        test_output,
        resolution,
        mult,
        call_count,
        expected_count,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        periodic = Periodic(bpm.resolution, test_output, mult=mult)

        for _ in range(call_count):
            bpm.update(now, periodic)

        assert test_output.call_count == expected_count
        assert test_output.on == is_even(expected_count)

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
        test_output,
        resolution,
        pwm,
        call_count,
        expected_on,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        periodic = Periodic(bpm.resolution, test_output, pwm=pwm)

        for _ in range(call_count):
            bpm.update(now, periodic)

        assert test_output.on == expected_on
