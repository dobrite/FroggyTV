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

# ~~~~~~~~~~ Initializing ~~~~~~~~~~~#

state = State()
screen_list = Screens(state)
encoder = Encoder()
play_button = Button(board.GP11).make_pin_reader()
page_button = Button(board.GP12).make_pin_reader()
encoder_button = Button(board.GP13).make_pin_reader()

# ~~~~~~~~~ Output Setup ~~~~~~~~~#
OUTPUT_LIST = [
    Output(0.5, 0.5, board.LED),
    Output(0.7, 0.7, board.GP1),
    Output(0.7, 0.7, board.GP2),
    Output(0.7, 0.7, board.GP3),
    Output(0.7, 0.7, board.GP4)]

# ~~~~~~~~~ Main Loop ~~~~~~~~~#

screen_list.show_current(state)

while True:
    now = time.monotonic()

    play_button.update()
    page_button.update()
    encoder_button.update()

    if play_button.rose:
        state.toggle_play()
        screen_list.screens[0].update_play_button(state.get_play())

    if page_button.rose:
        state.next_screen()

    if encoder_button.rose:
        state.next_element()
        screen_list.get_focused_screen(state).update_pointer(state)

    if state.get_focused_element() == 0:
        encoder.update(state.get_bpm())
        screen_list.get_focused_screen(state).update_bpm(state.get_bpm())
        OUTPUT_LIST[0].set_rate(state.get_bpm().bpm)

    elif state.get_focused_element() == 1:
        encoder.update(state.get_sync())
        screen_list.get_focused_screen(state).update_sync(state.get_sync())

    # Runs Outputs
    if state.get_play():
        for out in OUTPUT_LIST:
            out.toggle(now)

    # Displays Screens
    screen_list.show_current(state)
