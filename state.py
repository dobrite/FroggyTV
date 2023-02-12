SCREEN_NUMBER = 5 - 1 # Number of screens in use, may be changed later
ELEMENT_NUMBER = 3 - 1

class State():
    def __init__(self):
        self.play = True
        self.bpm = BPM()
        self.sync = Sync()
        self.focused_screen = 0
        self.focused_element = 0

    def get_focused_screen(self):
        return self.focused_screen

    def get_focused_element(self):
        return self.focused_element

    def next_screen(self):
        if self.focused_screen == SCREEN_NUMBER:
            self.focused_screen = 0 # Resets index to 0
        else:
            self.focused_screen += 1 # Increments index by 1

    def next_element(self):
        if self.focused_element == ELEMENT_NUMBER:
            self.focused_element = 0 # Resets index to 0
        else:
            self.focused_element += 1 # Increments index by 1

        print(self.focused_element)

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
class BPM():
    def __init__(self):
        self.bpm = 120

    def forward(self):
        if self.bpm < MAX_BPM: 
            self.bpm += 1

    def backwards(self):
        if self.bpm > MIN_BPM:
            self.bpm -= 1

class Sync():
    def __init__(self):
        self.sync = "Int"

    def forward(self):
        self.sync = "Ext"
        print("forwards")

    def backwards(self):
        self.sync = "Int"
        print("borwards")