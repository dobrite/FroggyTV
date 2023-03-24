class CountingTriggerable():
    def __init__(self):
        self.count = 0

    def trigger(self, _tick):
        self.count += 1
