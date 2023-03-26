class Debug:
    def __init__(self, debug):
        self.debug = debug
        self.count = 0
        self.prev_now = None
        self.elapsed = [0 for _ in range(1000)]

    def update(self, now):
        if not self.debug:
            return

        if self.prev_now:
            elapsed = now - self.prev_now
            self.elapsed[self.count] = elapsed

        self.count += 1
        self.prev_now = now

        if self.count == 1_000:
            self.count = 0
            avg = sum(self.elapsed) / len(self.elapsed)
            print(f"{avg / 1_000_000}ms")
