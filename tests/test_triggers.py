from froggytv.triggers import Periodic, Division, Noop, Counter
from helpers.utils import CallCounter, ImmediateBPM, FakeOutput, is_even
import pytest


class TestNoop:
    def test_ticking_noop_does_nothing(self):
        assert Noop().tick(0) is None

    def test_calling_noop_does_nothing(self):
        assert Noop()(0) is None


class TestDivision:
    @pytest.fixture
    def call_counter(self):
        return CallCounter()

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
    def test_division(self, call_counter, resolution, div, tick_count, expected_count):
        now = None
        bpm = ImmediateBPM(resolution)
        division = Division(call_counter, div)

        for _ in range(tick_count):
            bpm.update(now, division)

        assert call_counter.count == expected_count


class TestCounter:
    @pytest.fixture
    def call_counter(self):
        return FakeOutput()

    @pytest.mark.parametrize(
        "resolution, trigger_count, tick_count, expected_calls",
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
        self, call_counter, resolution, trigger_count, tick_count, expected_calls
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        counter = Counter(trigger_count, call_counter)

        for _ in range(tick_count):
            bpm.update(now, counter)

        assert call_counter.count == expected_calls


class TestPeriodic:
    @pytest.fixture
    def call_counter(self):
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
        call_counter,
        resolution,
        mult,
        call_count,
        expected_count,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        periodic = Periodic(bpm.resolution, call_counter, mult=mult)

        for _ in range(call_count):
            bpm.update(now, periodic)

        assert call_counter.count == expected_count
        assert call_counter.on == is_even(expected_count)

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
        call_counter,
        resolution,
        pwm,
        call_count,
        expected_on,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        periodic = Periodic(bpm.resolution, call_counter, pwm=pwm)

        for _ in range(call_count):
            bpm.update(now, periodic)

        assert call_counter.on == expected_on
