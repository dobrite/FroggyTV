class Noop:
    def __init__(self):
        pass

    def __call__(self, __tick__):
        pass

    def tick(self, __ticks__):
        pass


class FanOut:
    def __init__(self, collection):
        self._collection = collection

    def __call__(self, tick):
        for elem in self._collection:
            elem(tick)

    def tick(self, ticks):
        for elem in self._collection:
            elem.tick(ticks)


class Division:
    def __init__(self, tickable, div=1):
        self._tickable = tickable
        self._div = div
        self._count = 0

    def tick(self, tick):
        if self._count == 0:
            self._tickable.tick(tick)  # TODO

        self._count += 1

        if not self._count == self._div:
            return

        self._count = 0


class TicksToCall:
    def __init__(self, ticks_to_call, callable):
        self._ticks_to_call = ticks_to_call
        self._callable = callable
        self._count = 0

    def tick(self, tick):
        if self._count == 0:
            self._callable(tick)

        self._count += 1

        if self._count == self._ticks_to_call:
            self._count = 0


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
