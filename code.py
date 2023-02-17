# Frog Fractions Again!
# Designed by Izaak Hollander
# CC-BY-SA 4.0 I guess? Licenses are hard

import board
import time
from output import Output
from Screens import Screens
from hardware import Encoder, Button
from state import State

# ~~~~~~~~~~ Initializing ~~~~~~~~~~~#

state = State()
screens = [
    HomeScreen.make(state),
    GateScreen.make("A", state),
    GateScreen.make("B", state),
    GateScreen.make("C", state),
    GateScreen.make("D", state)
]
screen_list = Screens(state, screens)
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
    Output(0.7, 0.7, board.GP4)
]

# ~~~~~~~~~ Main Loop ~~~~~~~~~#

screen_list.show_current()

while True:
    now = time.monotonic()

    play_button.update()
    page_button.update()
    encoder_button.update()

    focused_screen = screen_list.get_focused_screen()
    focused_element = screen_list.get_focused_element()

    if play_button.rose:
        state.toggle_play()
        screen_list.screens[0].update_play_button(state.get_play())

    if page_button.rose:
        screen_list.next_screen()

    if encoder_button.rose:
        screen_list.next_element()
        focused_screen.update_pointer(focused_element)

    if focused_element == 0:
        encoder.update(state.get_bpm())
        focused_screen.update_bpm(state.get_bpm())
        OUTPUT_LIST[0].set_rate(state.get_bpm().bpm)
    elif focused_element == 1:
        encoder.update(state.get_sync())
        focused_screen.update_sync(state.get_sync())

    # Runs Outputs
    if state.get_play():
        for out in OUTPUT_LIST:
            out.toggle(now)

    # Displays Screens
    screen_list.show_current()
