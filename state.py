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
    def __init__(self):
        self.value = 5
        
        mult1 = [120, "x1"]
        mult2 = [60, "x2"]
        mult3 = [40, "x3"]
        mult4 = [15, "x4"]
        mult8 = [7.5, "x8"]
        mult16 = [3.75, "x16"]
        div2 = [240, "/2"]
        div3 = [360, "/3"]
        div4 = [480, "/4"]
        div8 = [960, "/8"]
        div16 = [1920, "/16"]

        self.divisions = [div16[0], div8[0], div4[0], div3[0], div2[0], mult1[0], mult2[0], mult3[0], mult4[0], mult8[0], mult16[0]]
        self.div_text = [div16[1], div8[1], div4[1], div3[1], div2[1], mult1[1], mult2[1], mult3[1], mult4[1], mult8[1], mult16[1]]

    def forward(self):
        prev = self.value
        if self.value < len(self.divisions) - 1: 
            self.value += 1

        return prev != self.value

    def backwards(self):
        prev = self.value
        if self.value > 0: 
            self.value -= 1

        return prev != self.value


