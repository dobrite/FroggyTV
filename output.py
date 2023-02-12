from digitalio import DigitalInOut, Direction, Pull

class Output():
    def __init__(self, on, off, pin):
        self.on = on
        self.off = off
        self.pin = DigitalInOut(pin)
        self.pin.direction = Direction.OUTPUT
        self.prev_time = -1

    def toggle(self, now):
        if self.pin.value is False:
            
            if now >= self.prev_time + self.off:
                    self.prev_time = now
                
                    self.pin.value = True
                        
        if self.pin.value is True:
                if now >= self.prev_time + self.on:
                    self.prev_time = now
                
                    self.pin.value = False

    def set_on(self, on):
        self.on = on

        

    