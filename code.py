# Frog Fractions Again!
# Designed by Izaak Hollander
# CC-BY-SA 4.0 I guess? Licenses are hard

import board
import time
import rotaryio
import random
from output import Output
from Screens import Screens, HomeScreen
from hardware import Encoder, Button
from state import State

#~~~~~~~~~~ Initializing ~~~~~~~~~~~#

state = State()
screen_list = Screens(state)
encoder = Encoder()
playbutton = Button(board.GP11).make_pin_reader()
pagebutton = Button(board.GP12).make_pin_reader()
encoderbutton = Button(board.GP13).make_pin_reader()

#~~~~~~~~~ Output Setup ~~~~~~~~~#
OUTPUT_LIST = [
    Output(0.5, 0.5, board.LED),
    Output(0.7, 0.7, board.GP1),
    Output(0.7, 0.7, board.GP2),
    Output(0.7, 0.7, board.GP3),
    Output(0.7, 0.7, board.GP4)]

#~~~~~~~~~ Main Loop ~~~~~~~~~#

screen_list.show_current(state)

while True:
    
    now = time.monotonic()

    playbutton.update()
    pagebutton.update()
    encoderbutton.update()

    if playbutton.rose:
        state.toggle_play()
        screen_list.screens[0].update_play_button(state.get_play())

    if pagebutton.rose:
        state.next_screen()

    if encoderbutton.rose:
        state.next_element()
        screen_list.get_focused_screen(state).update_pointer(state)

    #encoder.update(state.get_bpm())
    #screens.get_focused_screen(state).update_bpm(state.get_bpm())
    #OUTPUT_LIST[0].set_rate(state.get_bpm().bpm)

    # Runs Outputs
    if state.get_play():
        for out in OUTPUT_LIST:
            out.toggle(now)

    # Displays Screens
    screen_list.show_current(state)