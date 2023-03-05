# Frog Fractions Again!
# Designed by Izaak Hollander
# CC-BY-SA 4.0 I guess? Licenses are hard

import board
import time
import rp2pio
from Screens import Screens
from hardware import Button, Encoder, Output, OutputList
from state import State
from Screens import HomeScreen, GateScreen

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
    Output("home", 0.5, 0.5, board.LED),
    Output("A", 0.7, 0.7, board.GP1),
    Output("B", 0.7, 0.7, board.GP2),
    Output("C", 0.7, 0.7, board.GP3),
    Output("D", 0.7, 0.7, board.GP4)
]
output_list = OutputList(outputs)

# ~~~~~~~~~ Main Loop ~~~~~~~~~#

screen_list.show_current()

while True:

    # TODO async is what we gotta do: https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio/communicating-between-tasks#control-two-blinking-leds-3106381

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

    if encoder.update(focused_element.state):
        focused_element.update()
        if focused_element.screen == "home" and focused_element.name == "bpm":
            output_list.set_rate(state)
        elif focused_element.name == "div":  # TODO assumes only home OR gate screens exist
            output_list.set_rate(state)

    # Runs Outputs
    if state.get_play():
        output_list.update(now)
        screen_list.screens[0].froge.spin(now, state.get_bpm().value)

    # Displays Screens
    screen_list.show_current()
