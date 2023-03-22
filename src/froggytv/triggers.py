class Noop():
    def __init__(self):
        pass

    def trigger(self):
        pass


class FanOut():
    def __init__(self, triggers, final_trigger=Noop()):
        self._triggers = triggers
        self._final_trigger = final_trigger

    def trigger(self):
        for t in self._triggers:
            t.trigger()
        self._final_trigger.trigger()


class Periodic():
    def __init__(self, resolution, triggerable, mult=1):
        self._resolution = resolution
        self._triggerable = triggerable
        self._mult = mult
        self._next_mult = None
        self._count = 0

    def trigger(self):
        if self._count == 0:
            self._triggerable.trigger()

        self._count += 1

        if not self._count == self._trigger_count():
            return

        self._count = 0

        if not self._next_mult:
            return

        self._mult = self._next_mult
        self._next_mult = None

    def set_mult(self, mult):
        self._next_mult = mult

    def _trigger_count(self):
        return self._resolution / self._mult
