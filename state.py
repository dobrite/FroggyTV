class State():
    def __init__(self):
        self.play = True
        self.bpm = BPM()
        self.sync = Sync()
        self.div = Div()

    def get_play(self):
        return self.play

    def toggle_play(self):
        self.play = not self.play

    def get_bpm(self):
        return self.bpm

    def get_sync(self):
        return self.sync
    
    def get_div(self):
        return self.div


MAX_BPM = 500
MIN_BPM = 5
INT = "Int"
EXT = "Ext"


class BPM():
    def __init__(self):
        self.value = 120

    def forward(self):
        prev = self.value
        if self.value < MAX_BPM:
            self.value += 1

        return prev != self.value

    def backwards(self):
        prev = self.value
        if self.value > MIN_BPM:
            self.value -= 1

        return prev != self.value


class Sync():
    def __init__(self):
        self.value = INT

    def forward(self):
        prev = self.value
        self.value = EXT

        return prev != self.value

    def backwards(self):
        prev = self.value
        self.value = INT

        return prev != self.value

class Div():
    DIVISIONS = [ 
        3.75, # x16
        7.5, # x8
        15, # x4
        40, # x3
        60, # x2
        120, # x1
        240, # /2
        360, # /3
        480, # /4
        960, # /8
        1920 # /16
    ]   
    def __init__(self):
        self.index = 5  
        self.value = Div.DIVISIONS[self.index]

    def forward(self):
        prev = self.index
        if self.index < len(Div.DIVISIONS) - 1: 
            self.index += 1
            self.value = Div.DIVISIONS[self.index]

        return prev != self.index

    def backwards(self):
        prev = self.index
        if self.index > 0: 
            self.index -= 1
            self.value = Div.DIVISIONS[self.index]

        return prev != self.index


