from froggytv.triggers import Noop, Periodic
import pytest
from utils import CountingTriggerable


class TestNoop:
    def test_noop_does_nothing(self):
        assert Noop().trigger(0) is None


class TestPeriodic:
    @pytest.fixture
    def triggerable(self):
        return CountingTriggerable()

    @pytest.mark.parametrize("resolution, mult, trigger_count, expected", [
        (640, 1, 0, 0),
        (640, 1, 640, 1),
        (640, 1, 641, 2),
        (640, 2, 640, 2),
        (640, 2, 641, 3),
        (640, 2, 960, 3),
        (640, 2, 961, 4),
        (640, 0.5, 1280, 1),
        (640, 0.5, 1281, 2),
    ])
    def test_periodic(
        self,
        triggerable,
        resolution,
        mult,
        trigger_count,
        expected
    ):
        periodic = Periodic(resolution, triggerable, mult=mult)
        tick = 0

        for _ in range(trigger_count):
            periodic.trigger(tick)
            tick += 1
            if tick == resolution:
                tick = 0

        assert triggerable.count == expected
