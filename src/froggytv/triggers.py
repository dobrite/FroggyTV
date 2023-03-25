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


class Scaler:
    def __init__(self, resolution, tickable, scale=1):
        self._resolution = resolution
        self._tickable = tickable
        self._scale = scale
        self._last_tick = 0
        self._cycle_count = 0

    def tick(self, tick):
        if self._last_tick >= tick:
            self._cycle_count += 1
        self._last_tick = tick

        scaled_tick = self._scaled_tick(tick)
        if scaled_tick > self._resolution:
            self._cycle_count = 0
            scaled_tick = self._scaled_tick(tick)

        self._tickable.tick(scaled_tick)

    def _scaled_tick(self, tick):
        return (tick + (self._cycle_count * self._resolution)) * self._scale

    def _debug(self, tick, scaled_tick):
        print(
            "tick:",
            tick,
            "cycle_count:",
            self._cycle_count,
            "scaled_tick:",
            scaled_tick,
            "last_tick:",
            self._last_tick,
            "scale:",
            self._scale,
            "resolution:",
            self._resolution,
        )


class Counter:
    def __init__(self, trigger_count, callable=Noop()):
        self._trigger_count = trigger_count
        self._callable = callable
        self._final_callable = Noop()
        self._count = 0

    def set_final_callable(self, final_callable):
        self._final_callable = final_callable

    def __call__(self, tick):
        self._callable(tick)

    def tick(self, tick):
        if self._count == 0:
            self(tick)

        self._count += 1

        if self._count == self._trigger_count:
            self._count = 0
            self._final_callable(tick)


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


class Sequence:
    def __init__(self):
        self._index = 0
        self._callables = []

    def append(self, callable):
        self._callables.append(callable)

    def __call__(self, __tick__):
        self._index += 1
        if self._index == len(self._callables):
            self._index = 0

    def tick(self, tick):
        self._callables[self._index].tick(tick)
