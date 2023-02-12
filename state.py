class State():
    def __init__(self):
        self.play = True

    def get_play(self):
        return self.play

    def toggle_play(self):
        self.play = not self.play
