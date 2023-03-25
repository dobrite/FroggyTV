class Noop:
    def __init__(self):
        pass

    def tick(self, __ticks__):
        pass


class FanOut:
    def __init__(self, tickables):
        self._tickables = tickables

    def tick(self, ticks):
        for tickable in self._tickables:
            tickable.tick(ticks)


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
