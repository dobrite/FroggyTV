# Frog Fractions Again!
# Designed by Izaak Hollander
# CC-BY-SA 4.0 I guess? Licenses are hard

import board
import time
from digitalio import DigitalInOut, Direction, Pull
import rotaryio
import random
from output import Output
from Screens import Screens, HomeScreen
from hardware import Encoder
from state import State

#~~~~~~~~~~ Initializing ~~~~~~~~~~~#

state = State()
screen_list = Screens(state)
encoder = Encoder()

#------------------------------- Hardware Setup ------------------------------------#

# Setup Encoder Button
encoderbutton = DigitalInOut(board.GP13)
encoderbutton.direction = Direction.INPUT
encoderbutton.pull = Pull.UP
encoderbutton_state = None

# Setup Page Button
pagebutton = DigitalInOut(board.GP12)
pagebutton.direction = Direction.INPUT
pagebutton.pull = Pull.UP
pagebutton_state = None

# Setup start/stop Button (button3)
playbutton = DigitalInOut(board.GP11)
playbutton.direction = Direction.INPUT
playbutton.pull = Pull.UP
playbutton_state = None


#~~~~~~~~~ Output Setup ~~~~~~~~~#
OUTPUT_LIST = [
    Output(0.5, 0.5, board.LED),
    Output(0.7, 0.7, board.GP1),
    Output(0.7, 0.7, board.GP2),
    Output(0.7, 0.7, board.GP3),
    Output(0.7, 0.7, board.GP4)
]

#~~~~~~~~~ Main Loop ~~~~~~~~~#

screen_list.show_current(state)

while True:
    
    now = time.monotonic()


    # Play Button Logic
    if not playbutton.value and playbutton_state is None: 
        playbutton_state = "pressed"

    if playbutton.value and playbutton_state is "pressed":
        # print("Boop")
        state.toggle_play()
        screen_list.screens[0].update_play_button(state.get_play())
        playbutton_state = None

    # Button Logic
    if not pagebutton.value and pagebutton_state is None: 
        pagebutton_state = "pressed"

    if pagebutton.value and pagebutton_state is "pressed":
        state.next_screen()
        pagebutton_state = None

    #encoder.update(state.get_bpm())
    #screens.get_focused_screen(state).update_bpm(state.get_bpm())
    #OUTPUT_LIST[0].set_rate(state.get_bpm().bpm)

    
    # Runs Outputs
    if state.get_play():
        for out in OUTPUT_LIST:
            out.toggle(now)

    # Displays Screens
    screen_list.show_current(state)