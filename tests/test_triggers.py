from froggytv.triggers import Periodic, Division, Noop, Counter, Scaler
from helpers.utils import ImmediateBPM, is_even
import pytest


class TestNoop:
    def test_ticking_noop_does_nothing(self):
        assert Noop().tick(0) is None

    def test_calling_noop_does_nothing(self):
        assert Noop()(0) is None


class TestDivision:
    @pytest.mark.parametrize(
        "resolution, div, tick_call_count, expected_tick_call_count",
        [
            (640, 1, 0, 0),
            (640, 1, 1, 1),
            (640, 1, 640, 640),
            (640, 10, 640, 64),
            (640, 10, 6400, 640),
        ],
    )
    def test_division(
        self, test_output, resolution, div, tick_call_count, expected_tick_call_count
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        division = Division(test_output, div)

        for _ in range(tick_call_count):
            bpm.update(now, division)

        assert test_output.tick_call_count == expected_tick_call_count


class TestScaler:
    @pytest.mark.parametrize(
        "resolution, scale, tick_call_count, expected_tick_call_count, expected_ticks",
        [
            (640, 1, 1, 1, 1),
            (640, 1, 640, 640, 640),
            (640, 1, 641, 641, 1),
            (640, 1, 1280, 1280, 640),
            (640, 1, 1281, 1281, 1),
            (640, 10, 64, 64, 640),
            (640, 10, 640, 640, 6400),
            (640, 10, 641, 641, 10),
            (10, 0.1, 10, 10, 1),
            (10, 0.1, 20, 20, 2),
            (10, 0.1, 90, 90, 9),
            (10, 0.1, 100, 100, 10),
            (10, 0.1, 101, 101, 0.1),
            (640, 0.1, 640, 640, 64),
            (640, 0.1, 641, 641, 64.1),
            (640, 0.1, 649, 649, 64.9),
            (640, 0.1, 650, 650, 65),
            (640, 0.1, 6400, 6400, 640),
            (640, 0.1, 6401, 6401, 0.1),
            (640, 1 / 3, 640, 640, 213 + 1 / 3),
            (640, 1 / 3, 642, 642, 214),
            (640, 1 / 3, 1280, 1280, 426 + 2 / 3),
        ],
    )
    def test_scale(
        self,
        test_output,
        resolution,
        scale,
        tick_call_count,
        expected_tick_call_count,
        expected_ticks,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        division = Scaler(bpm.resolution, test_output, scale)

        for _ in range(tick_call_count):
            bpm.update(now, division)

        assert test_output.tick_call_count == expected_tick_call_count
        assert pytest.approx(test_output.ticks) == expected_ticks


class TestCounter:
    @pytest.mark.parametrize(
        "resolution, trigger_count, tick_call_count, expected_call_count",
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
        self,
        test_output,
        resolution,
        trigger_count,
        tick_call_count,
        expected_call_count,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        counter = Counter(trigger_count, test_output)

        for _ in range(tick_call_count):
            bpm.update(now, counter)

        assert test_output.call_count == expected_call_count


class TestPeriodic:
    @pytest.mark.parametrize(
        "resolution, mult, tick_call_count, expected_call_count",
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
        tick_call_count,
        expected_call_count,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        periodic = Periodic(bpm.resolution, test_output, mult=mult)

        for _ in range(tick_call_count):
            bpm.update(now, periodic)

        assert test_output.call_count == expected_call_count
        assert test_output.on == is_even(expected_call_count)

    @pytest.mark.parametrize(
        "resolution, pwm, tick_call_count, expected_on",
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
        tick_call_count,
        expected_on,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        periodic = Periodic(bpm.resolution, test_output, pwm=pwm)

        for _ in range(tick_call_count):
            bpm.update(now, periodic)

        assert test_output.on == expected_on
