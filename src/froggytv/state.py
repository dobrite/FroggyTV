ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]


class State:
    def __init__(self, gate_number):
        self.play = True
        self.state = {}
        self.state["home"] = {}
        self.state["home"] = {
            "div": Div(),
            "bpm": BPM(),
            "sync": Sync(),
        }
        for gate in ALPHABET[:gate_number]:
            self.state[gate] = {}
            self.state[gate] = {
                "div": Div(),
                "prob": Prob(),
                "pw": PW(),
            }

    def get_play(self):
        return self.play

    def toggle_play(self):
        self.play = not self.play

    def get_bpm(self):
        return self.state["home"]["bpm"]

    def get_sync(self):
        return self.state["home"]["sync"]

    def get_div(self, screen_name):
        return self.state[screen_name]["div"]

    def get_prob(self, screen_name):
        return self.state[screen_name]["prob"]

    def get_pw(self, screen_name):
        return self.state[screen_name]["pw"]


MAX_BPM = 300
MIN_BPM = 5
INT = "Int"
EXT = "Ext"


class BPM:
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


class Sync:
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


class Div:
    DIVISIONS = [
        1 / 64,
        1 / 32,
        1 / 16,
        1 / 8,
        1 / 5,
        1 / 4,
        1 / 3,
        1 / 2,
        1,
        2,
        3,
        4,
        5,
        8,
        16,
        32,
        64,
    ]

    def __init__(self):
        self.index = int(len(Div.DIVISIONS) / 2)
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


class Prob:
    def __init__(self):
        pass

    def forward(self):
        pass

    def backwards(self):
        pass


class PW:
    def __init__(self):
        pass

    def forward(self):
        pass

    def backwards(self):
        pass
