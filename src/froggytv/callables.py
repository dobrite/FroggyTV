class Noop:
    def __init__(self):
        pass

    def __call__(self, __tick__):
        pass


class FanOut:
    def __init__(self, callables):
        self._callables = callables

    def __call__(self, tick):
        for callable in self._callables:
            callable(tick)


class Periodic:
    def __init__(self, resolution, callable, mult=1, pwm=0.5):
        self._resolution = resolution
        self._callable = callable
        self._mult = mult
        self._next_mult = None
        self._pwm = pwm
        self._count = 0

    def tick(self, tick):
        if self._count == 0:
            self._callable(tick)

        self._count += 1

        if not self._count == self._call_count():
            return

        self._count = 0

        if not (self._next_mult and tick == 0):
            return

        self._mult = self._next_mult
        self._next_mult = None

    def set_mult(self, mult):
        self._next_mult = mult

    def _call_count(self):
        return self._resolution / self._mult / (1 / self._pwm)
