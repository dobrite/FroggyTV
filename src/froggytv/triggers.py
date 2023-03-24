class Noop:
    def __init__(self):
        pass

    def trigger(self, _tick):
        pass


class FanOut:
    def __init__(self, triggers, final_trigger=Noop()):
        self._triggers = triggers
        self._final_trigger = final_trigger

    def trigger(self, tick):
        for t in self._triggers:
            t.trigger(tick)
        self._final_trigger.trigger(tick)


class Periodic:
    def __init__(self, resolution, triggerable, mult=1):
        self._resolution = resolution
        self._triggerable = triggerable
        self._mult = mult
        self._next_mult = None
        self._count = 0

    def trigger(self, tick):
        if self._count == 0:
            self._triggerable.trigger(tick)

        self._count += 1

        if not self._count == self._trigger_count():
            return

        self._count = 0

        if not (self._next_mult and tick == 0):
            return

        self._mult = self._next_mult
        self._next_mult = None

    def set_mult(self, mult):
        self._next_mult = mult

    def _trigger_count(self):
        return self._resolution / self._mult / 2
