# Frog Fractions Again!
# Designed by Izaak Hollander
# CC-BY-SA 4.0 I guess? Licenses are hard

import board
import time

from bpm import Bpm
from debug import Debug
from hardware import Button, Encoder, Output, OutputList
from state import State, ALPHABET
from screens import HomeScreen, GateScreen, Screens
from triggers import FanOut, Periodic


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
triggers = [Periodic(bpm.resolution, outputs[i])
            for i, output in enumerate(outputs)]
fan_out = FanOut(triggers)

# ~~~~~~~~~ Main Loop ~~~~~~~~~#

screen_list.show_current()


debug = Debug(False)
while True:
    now = time.monotonic_ns()
    if not bpm.is_running():
        bpm.start(now)
    bpm.update(now, fan_out)
    debug.update(now)

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
        if focused_element.screen.name == "home" and focused_element.name == "bpm":
            bpm.set_bpm(state.get_bpm().value)
        elif focused_element.name == "div":
            triggers[ALPHABET.index(focused_element.screen.name)+1].set_mult(
                state.get_div(focused_element.screen.name).value)

    # Runs Outputs
    if state.get_play():
        # output_list.update(now)
        # screen_list.screens[0].froge.spin(now, state.get_bpm().value)
        pass
