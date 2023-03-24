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
