SCREEN_NUMBER = 4 # Number of screens in use, may be changed later

class State():
    def __init__(self):
        self.play = True
        self.bpm = BPM()
        self.focused_screen = 0
        self.focused_element = 0

    def get_focused(self):
        return self.focused_screen

    def next_screen(self):
        if self.focused_screen == SCREEN_NUMBER:
            self.focused_screen = 0 # Resets index to 0
        else:
            self.focused_screen += 1 # Increments index by 1

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
