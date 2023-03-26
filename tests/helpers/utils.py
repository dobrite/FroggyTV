from froggytv.bpm import Bpm
from froggytv.triggers import Noop


class TestOutput:
    def __init__(self):
        self.call_count = 0
        self.tick_call_count = 0
        self.ticks = 0
        self.on = False

    def tick(self, tick):
        self.tick_call_count += 1
        self.ticks = tick

    def __call__(self, __tick__):
        self.call_count += 1
        self.on = not self.on


class ImmediateBPM:
    def __init__(self, resolution=Bpm.DEFAULT_RESOLUTION):
        self.resolution = resolution
        self._tick = 0

    def update(self, __now__, tickable=Noop()):
        self._tick += 1
        if self._tick > self.resolution:
            self._tick = 1

        tickable.tick(self._tick)
