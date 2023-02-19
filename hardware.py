import board
from rotaryio import IncrementalEncoder
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer


class Encoder():
    def __init__(self):
        self.position = 0
        self.last_position = None
        self.encoder = IncrementalEncoder(board.GP14, board.GP15)

    def update(self, state):
        did_update = False
        self.position = self.encoder.position
        if self._moving_forward():
            did_update = state.forward()
        if self._moving_backwards():
            did_update = state.backwards()
        self.last_position = self.position

        return did_update

    def _moving_forward(self):
        return self.last_position is None or self.position > self.last_position

    def _moving_backwards(self):
        return self.last_position is None or self.position < self.last_position


class Button():
    def __init__(self, pin):
        self.button = DigitalInOut(pin)
        self.button.direction = Direction.INPUT
        self.button.pull = Pull.UP
        self.state = None

    def make_pin_reader(self):
        return Debouncer(lambda: self.button.value)


class Output():
    def __init__(self, on, off, pin):
        self.on = on
        self.off = off
        self.div = 4
        self.pin = DigitalInOut(pin)
        self.pin.direction = Direction.OUTPUT
        self.prev_time = -1

    def toggle(self, now):
        if not self.pin.value and now >= self.prev_time + self.off:
            self.prev_time = now
            self.pin.value = True

        if self.pin.value and now >= self.prev_time + self.on:
            self.prev_time = now
            self.pin.value = False

    def set_rate(self, bpm):
        self.on = (1 / bpm) * self.div
        self.off = (1 / bpm) * self.div
