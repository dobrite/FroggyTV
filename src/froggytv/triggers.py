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


class Scaler:
    def __new__(cls, resolution, tickable, scale):
        if scale >= 1:
            return Multiply(resolution, tickable, scale)
        else:
            return Divide(resolution, tickable, scale)


class Divide:
    def __init__(self, resolution, tickable, scale):
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
            "-> % remainder",
            scaled_tick % self._resolution,
        )


class Multiply:
    def __init__(self, resolution, tickable, scale):
        self._resolution = resolution
        self._tickable = tickable
        self._scale = scale

    def tick(self, tick):
        scaled_tick = tick * self._scale
        if scaled_tick % self._resolution == 0:
            self._tickable.tick(self._resolution)
        else:
            self._tickable.tick(scaled_tick % self._resolution)

    def _debug(self, tick, scaled_tick):
        print(
            "tick:",
            tick,
            "scaled_tick:",
            scaled_tick,
            "scale:",
            self._scale,
            "resolution:",
            self._resolution,
            "-> % remainder",
            scaled_tick % self._resolution,
        )


class Delay:
    def __init__(self, trigger_tick, callable=Noop()):
        self._trigger_tick = trigger_tick
        self._callable = callable
        self._last_tick = 1_000_000
        self._callable_called = False

    def tick(self, tick):
        if tick < self._last_tick:
            self._callable_called = False

        if not self._callable_called and tick >= self._trigger_tick:
            self._callable_called = True
            self._callable(tick)
        self._last_tick = tick


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


class PWM:
    def __init__(self, resolution, pwm, callable=Noop()):
        self._resolution = resolution
        self._pwm = pwm

        delay1 = Delay(1, callable)
        delay2 = Delay(round(resolution * pwm) + 1, callable)

        self._callable = FanOut([delay1, delay2])

    def __call__(self, __tick__):
        pass

    def tick(self, tick):
        self._callable.tick(tick)


class Gate:
    def __init__(self, output, resolution, scale, pwm):
        self._resolution = resolution
        self._output = output
        self._pwm = PWM(resolution, pwm, self._output)
        self._scaler = Scaler(self._resolution, self._pwm, scale)

    def set_scale(self, scale):
        self._scaler = Scaler(self._resolution, self._pwm, scale)

    def __call__(self, tick):
        self._scaler(tick)

    def tick(self, tick):
        self._scaler.tick(tick)
