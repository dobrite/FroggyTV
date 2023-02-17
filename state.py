SCREEN_NUMBER = 5 - 1  # Number of screens in use, may be changed later
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
            self.focused_screen = 0
        else:
            self.focused_screen += 1

    def next_element(self):
        if self.focused_element == ELEMENT_NUMBER:
            self.focused_element = 0
        else:
            self.focused_element += 1

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
