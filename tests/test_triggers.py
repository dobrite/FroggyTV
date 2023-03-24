from froggytv.triggers import Noop, Periodic
import pytest
from helpers.utils import FakeOutput, ImmediateBPM, is_even


class TestNoop:
    def test_noop_does_nothing(self):
        assert Noop().trigger(0) is None


class TestPeriodic:
    @pytest.fixture
    def triggerable(self):
        return FakeOutput()

    @pytest.mark.parametrize(
        "resolution, mult, trigger_count, expected_count",
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
        triggerable,
        resolution,
        mult,
        trigger_count,
        expected_count,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        periodic = Periodic(bpm.resolution, triggerable, mult=mult)

        for _ in range(trigger_count):
            bpm.update(now, periodic)

        assert triggerable.count == expected_count
        assert triggerable.on == is_even(expected_count)
