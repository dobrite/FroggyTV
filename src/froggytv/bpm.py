import math

try:
    from triggers import Noop
except ModuleNotFoundError:
    from froggytv.triggers import Noop


class Bpm:
    DEFAULT_RESOLUTION = 640
    NANOS_PER_SECOND = 1_000_000_000
    SECONDS_PER_MINUTE = 60

    def __init__(self, bpm, resolution=DEFAULT_RESOLUTION):
        self._bpm = bpm
        self._running = False
        self._tick = 0
        self.resolution = resolution

    def start(self, now):
        self._next_beat_at = now
        self._prev_beat_at = now - self._nanos_per_beat()
        self._tick = 0
        self._running = True

    def is_running(self):
        return self._running

    def update(self, now, tickable=Noop()):
        if now < self._next_beat_at:
            return

        tickable.tick(self._tick)

        self._step()

    def set_bpm(self, bpm):
        self._bpm = bpm
        self._npb = None
        self._next_beat_at = self._prev_beat_at + self._nanos_per_beat()

    def _step(self):
        self._tick += 1
        if self._tick > self.resolution:
            self._tick = 1

        self._prev_beat_at = self._next_beat_at
        self._next_beat_at = self._prev_beat_at + self._npb

    def _nanos_per_beat(self):
        self._npb = math.floor(self._seconds_per_beat() * Bpm.NANOS_PER_SECOND)
        return self._npb

    def _seconds_per_beat(self):
        return Bpm.SECONDS_PER_MINUTE / self._bpm / self.resolution
