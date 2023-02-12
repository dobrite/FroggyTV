import board
from rotaryio import IncrementalEncoder

class Encoder():
    def __init__(self):
        self.position = 0
        self.last_position = None
        self.encoder = IncrementalEncoder(board.GP14, board.GP15)

    def update(self,element):
        self.position = self.encoder.position
        if self._moving_forward():
            element.add()

        if self._moving_backwards():
            element.subtract()

        self.last_position = self.position

    def _moving_forward(self):
        return self.last_position is None or self.position > self.last_position

    def _moving_backwards(self):
        return self.last_position is None or self.position < self.last_position