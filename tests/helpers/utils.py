from froggytv.bpm import Bpm, Noop


def is_even(num):
    return num % 2


class CountingTickable:
    def __init__(self):
        self.count = 0

    def tick(self, __tick__):
        self.count += 1


class FakeOutput:
    def __init__(self):
        self.count = 0
        self.on = False

    def __call__(self, __tick__):
        self.count += 1
        self.on = not self.on


class ImmediateBPM:
    def __init__(self, resolution=Bpm.DEFAULT_RESOLUTION):
        self.resolution = resolution
        self._tick = 0

    def update(self, __now__, tickable=Noop()):
        self._tick += 1
        if self._tick == self.resolution:
            self._tick = 0

        tickable.tick(self._tick)
