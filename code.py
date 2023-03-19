# Frog Fractions Again!
# Designed by Izaak Hollander
# CC-BY-SA 4.0 I guess? Licenses are hard

import board
import time

from bpm import Bpm
from hardware import Button, Encoder, Output, OutputList
from state import State
from screens import HomeScreen, GateScreen, Screens

# ~~~~~~~~~~ Initializing ~~~~~~~~~~~#

state = State(4)
screens = [
    HomeScreen.make("home", state),
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

outputs = [
    Output("home", board.LED),
    Output("A", board.GP1),
    Output("B", board.GP2),
    Output("C", board.GP3),
    Output("D", board.GP4)
]
output_list = OutputList(outputs)
bpm = Bpm(120)

# ~~~~~~~~~ Main Loop ~~~~~~~~~#

screen_list.show_current()

while True:
    now = time.monotonic_ns()

    play_button.update()
    page_button.update()
    encoder_button.update()

    if play_button.rose:
        state.toggle_play()
        screen_list.screens[0].update_play_button(state.get_play())

    if page_button.rose:
        screen_list.next_screen()

    if encoder_button.rose:
        screen_list.next_element()

    focused_element = screen_list.get_focused_element()
    if encoder.update(focused_element.state):
        focused_element.update()

        # TODO assumes only home OR gate screens exist
        if focused_element.screen == "home" and focused_element.name == "bpm":
            pass  # TODO: set bpm
        elif focused_element.name == "div":
            pass  # TODO: set mult

    # Runs Outputs
    if state.get_play():
        # output_list.update(now)
        # screen_list.screens[0].froge.spin(now, state.get_bpm().value)
        pass
