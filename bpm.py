import math

import triggers


class Bpm():
    DEFAULT_RESOLUTION = 24
    NANOS_PER_SECOND = 1_000_000_000
    SECONDS_PER_MINUTE = 60

    def __init__(self, bpm, resolution=DEFAULT_RESOLUTION):
        self._bpm = bpm
        self._running = False
        self.resolution = resolution

    def start(self, now):
        self._next_beat_at = now
        self._prev_beat_at = now - self._nanos_per_beat()
        self._running = True

    def resolution(self):
        return self.resolution

    def is_running(self):
        return self._running

    def update(self, now, triggerable=triggers.Noop()):
        if now < self._next_beat_at:
            return

        triggerable.trigger()

        self._step()

    def set_bpm(self, bpm):
        self._bpm = bpm
        self._next_beat_at = self._calc_next_beat_at()

    def _step(self):
        self._prev_beat_at = self._next_beat_at
        self._next_beat_at = self._calc_next_beat_at()

    def _calc_next_beat_at(self):
        return self._prev_beat_at + self._nanos_per_beat()

    def _nanos_per_beat(self):
        return math.floor(self._seconds_per_beat() * Bpm.NANOS_PER_SECOND)

    def _seconds_per_beat(self):
        return Bpm.SECONDS_PER_MINUTE / self._bpm / self.resolution
