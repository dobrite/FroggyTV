from adafruit_debouncer import Debouncer
import board
from digitalio import DigitalInOut, Direction, Pull
from rotaryio import IncrementalEncoder


class Encoder:
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


class Button:
    def __init__(self, pin):
        self.button = DigitalInOut(pin)
        self.button.direction = Direction.INPUT
        self.button.pull = Pull.UP
        self.state = None

    def make_pin_reader(self):
        return Debouncer(lambda: self.button.value)


class Output:
    def __init__(self, name, pin):
        self._name = name
        self._pin = DigitalInOut(pin)
        self._pin.direction = Direction.OUTPUT

    def __call__(self, __tick__):
        # TODO: needs called twice per mult for 50% PWM
        self._pin.value = not self._pin.value
