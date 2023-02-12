class State():
    def __init__(self):
        self.play = True
        self.bpm = BPM()

    def get_play(self):
        return self.play

    def toggle_play(self):
        self.play = not self.play

    def get_bpm(self):
        return self.bpm


MAX_BPM = 500
MIN_BPM = 5
class BPM():
    def __init__(self):
        self.bpm = 120

    def forward(self):
        if self.bpm < MAX_BPM: 
            self.bpm += 1

    def backwards(self):
        if self.bpm > MIN_BPM:
            self.bpm -= 1