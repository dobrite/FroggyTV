class State():
    def __init__(self):
        self.play = True
        self.bpm = BPM()
        self.sync = Sync()

    def get_play(self):
        return self.play

    def toggle_play(self):
        self.play = not self.play

    def get_bpm(self):
        return self.bpm

    def get_sync(self):
        return self.sync


MAX_BPM = 500
MIN_BPM = 5
INT = "Int"
EXT = "Ext"


class BPM():
    def __init__(self):
        self.value = 120

    def forward(self):
        if self.value < MAX_BPM:
            self.value += 1

    def backwards(self):
        if self.value > MIN_BPM:
            self.value -= 1


class Sync():
    def __init__(self):
        self.value = INT

    def forward(self):
        self.value = EXT

    def backwards(self):
        self.value = INT
