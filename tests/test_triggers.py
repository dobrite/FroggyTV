from froggytv.triggers import (
    Counter,
    Delay,
    Gate,
    Noop,
    PWM,
    Scaler,
    Sequence,
)
from helpers.utils import ImmediateBPM
import pytest


class TestNoop:
    def test_ticking_noop_does_nothing(self):
        assert Noop().tick(0) is None

    def test_calling_noop_does_nothing(self):
        assert Noop()(0) is None


class TestScaler:
    @pytest.mark.parametrize(
        "resolution, scale, tick_call_count, expected_tick_call_count, expected_ticks",
        [
            (640, 1, 1, 1, 1),
            (640, 1, 640, 640, 640),
            (640, 1, 641, 641, 1),
            (640, 1, 1280, 1280, 640),
            (640, 1, 1281, 1281, 1),
            (640, 2, 320, 320, 640),
            (640, 2, 321, 321, 2),
            (640, 2, 640, 640, 640),
            (640, 2, 641, 641, 2),
            (640, 10, 64, 64, 640),
            (640, 10, 640, 640, 640),
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
        scaler = Scaler(bpm.resolution, test_output, scale)

        for _ in range(tick_call_count):
            bpm.update(now, scaler)

        assert test_output.tick_call_count == expected_tick_call_count
        assert pytest.approx(test_output.ticks) == expected_ticks


class TestDelay:
    @pytest.mark.parametrize(
        "resolution, trigger_tick, tick_call_count, expected_call_count",
        [
            (640, 10, 0, 0),
            (640, 10, 1, 0),
            (640, 10, 9, 0),
            (640, 10, 10, 1),
            (640, 10, 11, 1),
            (640, 10, 640, 1),
            (640, 10, 641, 1),
            (640, 10, 649, 1),
            (640, 10, 650, 2),
            (640, 10, 651, 2),
            (640, 32, 0, 0),
            (640, 32, 1, 0),
            (640, 32, 31, 0),
            (640, 32, 32, 1),
            (640, 32, 33, 1),
            (640, 32, 640, 1),
            (640, 32, 641, 1),
            (640, 32, 671, 1),
            (640, 32, 672, 2),
            (640, 32, 673, 2),
        ],
    )
    def test_delay(
        self,
        test_output,
        resolution,
        trigger_tick,
        tick_call_count,
        expected_call_count,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        delay = Delay(trigger_tick, test_output)

        for _ in range(tick_call_count):
            bpm.update(now, delay)

        assert test_output.call_count == expected_call_count


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


class TestPWM:
    @pytest.mark.parametrize(
        "resolution, pwm, tick_call_count, expected_call_count, expected_on",
        [
            (640, 0.5, 0, 0, False),
            (640, 0.5, 1, 1, True),
            (640, 0.5, 319, 1, True),
            (640, 0.5, 320, 1, True),
            (640, 0.5, 321, 2, False),
            (640, 0.5, 640, 2, False),
            (640, 0.5, 641, 3, True),
            (640, 0.1, 0, 0, False),
            (640, 0.1, 1, 1, True),
            (640, 0.1, 63, 1, True),
            (640, 0.1, 64, 1, True),
            (640, 0.1, 65, 2, False),
            (640, 0.1, 640, 2, False),
            (640, 0.1, 641, 3, True),
            (640, 0.9, 0, 0, False),
            (640, 0.9, 1, 1, True),
            (640, 0.9, 575, 1, True),
            (640, 0.9, 576, 1, True),
            (640, 0.9, 577, 2, False),
            (640, 0.9, 640, 2, False),
            (640, 0.9, 641, 3, True),
        ],
    )
    def test_pwm(
        self,
        test_output,
        resolution,
        pwm,
        tick_call_count,
        expected_call_count,
        expected_on,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        pwm = PWM(resolution, pwm, test_output)

        for _ in range(tick_call_count):
            bpm.update(now, pwm)

        assert test_output.on == expected_on
        assert test_output.call_count == expected_call_count


class TestSequence:
    @pytest.mark.parametrize(
        "resolution, tick_call_count, expected_call_count, expected_on",
        [
            (640, 0, 0, False),
            (640, 1, 1, True),
            (640, 9, 1, True),
            (640, 10, 1, True),
            (640, 11, 2, False),
            (640, 21, 2, False),
            (640, 30, 2, False),
            (640, 31, 3, True),
        ],
    )
    def test_sequence(
        self, test_output, resolution, tick_call_count, expected_call_count, expected_on
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        counter1 = Counter(10, test_output)
        counter2 = Counter(20, test_output)
        sequence = Sequence()
        sequence.append(counter1)
        sequence.append(counter2)
        counter1.set_final_callable(sequence)
        counter2.set_final_callable(sequence)

        for _ in range(tick_call_count):
            bpm.update(now, sequence)

        assert test_output.on == expected_on
        assert test_output.call_count == expected_call_count


class TestGate:
    @pytest.mark.parametrize(
        "resolution, scale, pwm, tick_call_count, expected_call_count, expected_on",
        [
            (640, 1, 0.5, 0, 0, False),
            (640, 1, 0.5, 1, 1, True),
            (640, 1, 0.5, 319, 1, True),
            (640, 1, 0.5, 320, 1, True),
            (640, 1, 0.5, 321, 2, False),
            (640, 1, 0.5, 640, 2, False),
            (640, 1, 0.5, 641, 3, True),
            (640, 1, 0.1, 0, 0, False),
            (640, 1, 0.1, 1, 1, True),
            (640, 1, 0.1, 63, 1, True),
            (640, 1, 0.1, 64, 1, True),
            (640, 1, 0.1, 65, 2, False),
            (640, 1, 0.1, 640, 2, False),
            (640, 1, 0.1, 641, 3, True),
            (640, 2, 0.5, 0, 0, False),
            (640, 2, 0.5, 1, 1, True),
            (640, 2, 0.5, 159, 1, True),
            (640, 2, 0.5, 160, 1, True),
            (640, 2, 0.5, 161, 2, False),
            (640, 2, 0.5, 319, 2, False),
            (640, 2, 0.5, 320, 2, False),
            (640, 2, 0.5, 321, 3, True),
            (640, 2, 0.5, 479, 3, True),
            (640, 2, 0.5, 480, 3, True),
            (640, 2, 0.5, 481, 4, False),
        ],
    )
    def test_gate(
        self,
        test_output,
        resolution,
        scale,
        pwm,
        tick_call_count,
        expected_call_count,
        expected_on,
    ):
        now = None
        bpm = ImmediateBPM(resolution)
        gate = Gate(test_output, bpm.resolution, scale, pwm)

        for _ in range(tick_call_count):
            bpm.update(now, gate)

        assert test_output.on == expected_on
        assert test_output.call_count == expected_call_count
