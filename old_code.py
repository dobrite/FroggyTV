# Frog Fractions!
# Designed by Izaak Hollander
# CC-BY-SA 4.0 I guess? Licenses are hard

import board
import displayio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import busio
from adafruit_bitmap_font import bitmap_font
import time
from digitalio import DigitalInOut, Direction, Pull
import rotaryio
import random

# ------------------------------- Screen Setup ------------------------------------#

displayio.release_displays()

spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
oled_reset = board.GP20

# Use for SPI
oled_cs = board.GP17
oled_dc = board.GP16
display_bus = displayio.FourWire(
    spi, command=oled_dc, chip_select=oled_cs, reset=oled_reset, baudrate=1000000
)

WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 0


display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000  # Black

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)


# ------------------------------- Hardware Setup ------------------------------------#


# Setup Encoder
encoder = rotaryio.IncrementalEncoder(board.GP14, board.GP15)
last_position = None

# Setup Encoder Button (button1)
button1 = DigitalInOut(board.GP13)
button1.direction = Direction.INPUT
button1.pull = Pull.UP

button1_state = None

# Setup Page Button (button2)
button2 = DigitalInOut(board.GP12)
button2.direction = Direction.INPUT
button2.pull = Pull.UP

button2_state = None

# Setup start/stop Button (button3)
button3 = DigitalInOut(board.GP11)
button3.direction = Direction.INPUT
button3.pull = Pull.UP

button3_state = None

# Setup Sync Input
clk_in = DigitalInOut(board.GP28)
clk_in.direction = Direction.INPUT
clk_in.pull = Pull.UP

clk_in_state = None

# Defines each output! Don't change PREV_TIME

OUTPUT_LIST = [
    {"ON": 0.5, "OFF": 0.5, "PREV_TIME": -1, "PIN": board.LED, "PROB": 100},
    {"ON": 0.25, "OFF": 0.25, "PREV_TIME": -1, "PIN": board.GP1, "PROB": 50},
    {"ON": 0.25, "OFF": 0.25, "PREV_TIME": -1, "PIN": board.GP2, "PROB": 100},
    {"ON": 0.25, "OFF": 0.25, "PREV_TIME": -1, "PIN": board.GP3, "PROB": 100},
    {"ON": 0.25, "OFF": 0.25, "PREV_TIME": -1, "PIN": board.GP4, "PROB": 100},
    {"ON": 0.25, "OFF": 0.25, "PREV_TIME": -1, "PIN": board.GP5, "PROB": 100},
]

# Defines output pins
for out in OUTPUT_LIST:
    out["PIN"] = DigitalInOut(out["PIN"])
    out["PIN"].direction = Direction.OUTPUT

    # Add LED Pull at some point, not sure if up or down

# To add: Piezo buzzer, Piezo Level?? -- Could be hardware trimmer

# ------------------------------- GUI Setup ------------------------------------#

# ~~~~~~~~~~ Fonts ~~~~~~~~~~#

# Import Fonts
smolfont = bitmap_font.load_font("/Fonts/FrogPrincess-7.pcf")
biggefont = bitmap_font.load_font("/Fonts/FrogPrincess-10.pcf")

# ~~~~~~~ Menu Elements ~~~~~~~#

# Menu Element list
elements = ["BPMedit", "Syncedit", "Divedit"]  # , "PWedit"] #"DivAedit"]
# Pointer Position list
pointer_positions = [[1, 5], [1, 25], [5, 43], [69, 43], [65, 5]]

# Sets the currently selected menu element
elem_index = 0

active_element = elements[elem_index]


# ~~~~~~~ Home Screen ~~~~~~~#

# Creates the home screen
homeScreen = displayio.Group()

# Initial BPM text
BPMText = "120"
BPMtext_area = label.Label(biggefont, text=BPMText, color=0xFFFFFF, x=20, y=35 // 2 - 1)
homeScreen.append(BPMtext_area)

# Creates Label "BPM" in smaller font
BPMLabeltext_area = label.Label(
    smolfont, text="BPM", color=0xFFFFFF, x=69, y=35 // 2 - 1
)
homeScreen.append(BPMLabeltext_area)


# Creates Label "Int" in smaller font
SyncLabeltext_area = label.Label(
    smolfont, text="INT", color=0xFFFFFF, x=20, y=77 // 2 - 1
)
homeScreen.append(SyncLabeltext_area)

# Initial Division text
DivText = "x1"
Divtext_area = label.Label(smolfont, text=DivText, color=0xFFFFFF, x=28, y=110 // 2 - 1)
homeScreen.append(Divtext_area)


# ~~~~~~~ Gate Screen Label Positions ~~~~~~~~#
# Moves gate screen labels together for easier editing

gateScreenIconx = 5
gateScreenIcony = 30
gateScreenDivx = 105
gateScreenDivy = 30

# ~~~~~~~ Gate Screen A ~~~~~~~~#

# Creates the "A" gate screen
gateScreenA = displayio.Group()

# Text icon
LabelAtext_area = label.Label(
    biggefont, text="A", color=0xFFFFFF, x=gateScreenIconx, y=gateScreenIcony // 2 - 1
)
gateScreenA.append(LabelAtext_area)

# A Division text
DivAText = "x1"
DivAtext_area = label.Label(
    smolfont, text=DivAText, color=0xFFFFFF, x=gateScreenDivx, y=gateScreenDivy // 2 - 1
)
gateScreenA.append(DivAtext_area)


# ~~~~~~~ Gate Screen B ~~~~~~~~#

# Creates the "B" gate screen
gateScreenB = displayio.Group()

# Text icon
LabelBtext_area = label.Label(
    biggefont, text="B", color=0xFFFFFF, x=gateScreenIconx, y=gateScreenIcony // 2 - 1
)
gateScreenB.append(LabelBtext_area)

# B Division text
DivBText = "x1"
DivBtext_area = label.Label(
    smolfont, text=DivBText, color=0xFFFFFF, x=gateScreenDivx, y=gateScreenDivy // 2 - 1
)
gateScreenB.append(DivBtext_area)


# ~~~~~~~ Gate Screen C ~~~~~~~~#

# Creates the "C" gate screen
gateScreenC = displayio.Group()

# Text icon
LabelCtext_area = label.Label(
    biggefont, text="C", color=0xFFFFFF, x=gateScreenIconx, y=gateScreenIcony // 2 - 1
)
gateScreenC.append(LabelCtext_area)

# C Division text
DivCText = "x1"
DivCtext_area = label.Label(
    smolfont, text=DivCText, color=0xFFFFFF, x=gateScreenDivx, y=gateScreenDivy // 2 - 1
)
gateScreenC.append(DivCtext_area)

# ~~~~~~~ Gate Screen D ~~~~~~~~#

# Creates the "D" gate screen
gateScreenD = displayio.Group()

# Text icon
LabelDtext_area = label.Label(
    biggefont, text="D", color=0xFFFFFF, x=gateScreenIconx, y=gateScreenIcony // 2 - 1
)
gateScreenD.append(LabelDtext_area)

# D Division text
DivDText = "x1"
DivDtext_area = label.Label(
    smolfont, text=DivDText, color=0xFFFFFF, x=gateScreenDivx, y=gateScreenDivy // 2 - 1
)
gateScreenD.append(DivDtext_area)

# ~~~~~~~~~~ Screen Indexing ~~~~~~~~~~~#

Screens = [homeScreen, gateScreenA, gateScreenB, gateScreenC, gateScreenD]

screen_index = 0

currentScreen = Screens[screen_index]


# ~~~~~~~ Menu Elements ~~~~~~~~#

# Draws the pointer icon
pointer = displayio.OnDiskBitmap("/Icons/pointer.bmp")
pointer_area = displayio.TileGrid(pointer, pixel_shader=pointer.pixel_shader)
pointer_group = displayio.Group()
pointer_group.append(pointer_area)
# Pointer positions
pointer_group.x = pointer_positions[elem_index][0]
pointer_group.y = pointer_positions[elem_index][1]
currentScreen.append(pointer_group)


# Draws the pwm sprite
pwmsprite_sheet = displayio.OnDiskBitmap("/Icons/PWMSpritesheetSmol.bmp")
pwmsprite = displayio.TileGrid(
    pwmsprite_sheet,
    pixel_shader=pwmsprite_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=13,  # Determines sprite size, Bigge tile is 41x22, Smol tile is 13x8
    tile_height=8,
)
pwmsprite_group = displayio.Group(scale=2)
pwmsprite_group.append(pwmsprite)
# PW icon positions
pwmsprite_group.x = 85
pwmsprite_group.y = 40
# currentScreen.append(pwmsprite_group)

# Draws the stage
stage = displayio.OnDiskBitmap("/Icons/stage.bmp")
stagegrid = displayio.TileGrid(
    stage,
    pixel_shader=stage.pixel_shader,
)
stage_group = displayio.Group()
stage_group.append(stagegrid)
# PW icon positions
stage_group.x = 81
stage_group.y = 50
homeScreen.append(stage_group)

# Draws froge
frogesprite_sheet = displayio.OnDiskBitmap("/Icons/SpinSpritesheet.bmp")
frogesprite = displayio.TileGrid(
    frogesprite_sheet,
    pixel_shader=frogesprite_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=22,  # Determines sprite size, Bigge tile is 41x22, Smol tile is 13x8
    tile_height=22,
)
frogesprite_group = displayio.Group(scale=1)
frogesprite_group.append(frogesprite)
# froge positions
frogesprite_group.x = 80
frogesprite_group.y = 30
# Comment to hide froge <-------------------------------------------------------
homeScreen.append(frogesprite_group)

froge_spin = False


# Draws play/pause
playsprite_sheet = displayio.OnDiskBitmap("/Icons/playpause.bmp")
playsprite = displayio.TileGrid(
    playsprite_sheet,
    pixel_shader=playsprite_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=16,  # Determines sprite size, Bigge tile is 41x22, Smol tile is 13x8
    tile_height=16,
)
playsprite_group = displayio.Group(scale=1)
playsprite_group.append(playsprite)
# froge positions
playsprite_group.x = 55
playsprite_group.y = 35
homeScreen.append(playsprite_group)


# ------------------------------- Clock Setup ------------------------------------#

# Time stuff
now = time.monotonic()


# ~~~~~~~ Divisions ~~~~~~~~#

# Set clock divisions (add more in the future)
mult1 = [120, "x1"]
mult2 = [60, "x2"]
mult3 = [40, "x3"]
mult4 = [15, "x4"]
mult8 = [7.5, "x8"]
mult16 = [3.75, "x16"]
div2 = [240, "/2"]
div3 = [360, "/3"]
div4 = [480, "/4"]
div8 = [960, "/8"]
div16 = [1920, "/16"]

# Clock Division list
divisions = [
    div16[0],
    div8[0],
    div4[0],
    div3[0],
    div2[0],
    mult1[0],
    mult2[0],
    mult3[0],
    mult4[0],
    mult8[0],
    mult16[0],
]

divisionsText = [
    div16[1],
    div8[1],
    div4[1],
    div3[1],
    div2[1],
    mult1[1],
    mult2[1],
    mult3[1],
    mult4[1],
    mult8[1],
    mult16[1],
]


# ~~~~~~~ Tempo/Rate/Div/PW on startup ~~~~~~~~#

# Base Tempo on startup
beatsperminute = 120

# Base clock rates on startup
base_clock_rate = 0.5
A_clock_rate = 0.5

# Base Divisions on startup
basediv = 5  # Set this to the index of mult1
Adiv = 5

# Sets initial pulse width
baseRisePW = 0.5
baseFallPW = 0.5
pw_index = 5  # Sets initial Pulse width Sprite (50%)


# Sets time division froge spins at
spin_rate = 15
froge_index = 0  # Sets initial froge sprite

# Makes the clock run on startup
play = True
play_index = 0  # Sets initial play sprite


# Makes sure trigger mode is initially false
Trig_mode = False
# Makes initial sync internal
sync_mode = False

# Sets random seed
random.seed(66)


last_clk = time.monotonic()
interval = 0.5

# ------------------------------- Main Loop -----------------------------------#


while True:
    now = time.monotonic()

    if play is True:
        # Sets the rate for all outputs!! Super slick
        if sync_mode is False:
            for out in OUTPUT_LIST:
                # rng = random.randrange(0,100,1)
                if out["PIN"].value is False:
                    if now >= out["PREV_TIME"] + out["OFF"]:
                        out["PREV_TIME"] = now

                        out["PIN"].value = True

                if out["PIN"].value is True:
                    if now >= out["PREV_TIME"] + out["ON"]:
                        out["PREV_TIME"] = now

                        out["PIN"].value = False

        if sync_mode is True:
            for out in OUTPUT_LIST:
                if now > out["PREV_TIME"] + interval:
                    out["PREV_TIME"] = now

                    out["PIN"].value = True
                else:
                    out["PIN"].value = False

        # Horrible sync stuff, not working rn

        if not clk_in.value and clk_in_state is None:  # Button stuff
            clk_in_state = "pressed"

        if button1.value and button1_state == "pressed":
            interval = now - last_clk
            last_clk = now

        # Spins froge around wheeeee
        if froge_spin is False:
            if now >= out["PREV_TIME"] + (1 / beatsperminute) * spin_rate:
                if froge_index != 7:
                    froge_index = froge_index + 1
                else:
                    froge_index = 0
                out["PREV_TIME"] = now
                froge_spin = True
        # Needs a True and False loop just so that he syncs up right
        if froge_spin is True:
            if now >= out["PREV_TIME"] + (1 / beatsperminute) * spin_rate:
                if froge_index != 7:
                    froge_index = froge_index + 1
                else:
                    froge_index = 0
                out["PREV_TIME"] = now
                froge_spin = False
    else:
        pass  # Stops the clock

    # Determines the clock rates based on BPM and time division
    base_clock_rate = (1 / beatsperminute) * divisions[basediv]

    A_clock_rate = (1 / beatsperminute) * divisions[Adiv]

    # Init definiteion of encoder position
    position = encoder.position

    # Encoder is moving clockwise (forward)
    # Adds to either BPM or Div, depending on which is selected
    if last_position is None or position > last_position:
        # BPM Add
        if active_element == "BPMedit":
            beatsperminute = beatsperminute + 1
            if beatsperminute > 500:  # Sets maximum BPM
                beatsperminute = 500
        # Div Add
        elif active_element == "Divedit":
            if basediv < len(divisions) - 1:
                basediv = basediv + 1
            else:
                pass
        # Pulse Width Add
        elif active_element == "PWedit":
            # Changes Sprite
            pw_index = pw_index + 1
            if pw_index > 9:
                pw_index = 9
            elif pw_index != 0:
                Trig_mode = False  # Disables Trigger mode
            # Changes Rise
            baseRisePW = baseRisePW + 0.1
            if baseRisePW > 0.9:
                baseRisePW = 0.9
            # Changes Fall
            baseFallPW = baseFallPW - 0.1
            if baseRisePW < 0.1:
                baseRisePW = 0.1
        elif active_element == "Syncedit":
            if sync_mode is False:
                SyncLabeltext_area.text = "EXT"
                sync_mode = True
            else:
                SyncLabeltext_area.text = "INT"
                sync_mode = False

    # Encoder is moving counter-clockwise (back)
    # Subtracts from either BPM or Div, depending on which is selected
    if last_position is None or position < last_position:
        # BPM Subtract
        if active_element == "BPMedit":
            beatsperminute = beatsperminute - 1
            if beatsperminute < 20:  # Sets minimum BPM
                beatsperminute = 20
        # Div Subtract
        elif active_element == "Divedit":
            if basediv > 0:
                basediv = basediv - 1
            else:
                pass
        # Pulse Width Subtract
        elif active_element == "PWedit":
            # Changes Sprite
            pw_index = pw_index - 1
            if pw_index < 0:
                pw_index = 0
            elif pw_index == 0:
                Trig_mode = True  # Enables Trigger mode

            # Changes Rise
            baseRisePW = baseRisePW - 0.1
            if baseRisePW < 0.1:
                baseRisePW = 0.1
            # Changes Fall
            baseFallPW = baseFallPW + 0.1
            if baseRisePW > 0.9:
                baseRisePW = 0.9

        elif active_element == "Syncedit":
            if sync_mode is False:
                SyncLabeltext_area.text = "EXT"
                sync_mode = True
            else:
                SyncLabeltext_area.text = "INT"
                sync_mode = False

    last_position = position  # Encoder stuff

    active_element = elements[elem_index]

    # Trigger mode: If Trigger mode is enabled,
    if Trig_mode is False:
        OUTPUT_LIST[0]["ON"] = baseRisePW * base_clock_rate
        OUTPUT_LIST[0]["OFF"] = baseFallPW * base_clock_rate

    if Trig_mode is True:
        OUTPUT_LIST[0]["ON"] = 0.01
        OUTPUT_LIST[0]["OFF"] = base_clock_rate - 0.01

    # Encoder button functions
    if not button1.value and button1_state is None:  # Button stuff
        button1_state = "pressed"

    if (
        button1.value and button1_state == "pressed"
    ):  # Increments the menu element index
        if elem_index != len(elements) - 1:
            elem_index = elem_index + 1  # Increments index by 1
        elif elem_index == len(elements) - 1:
            elem_index = 0  # Resets index to 0

        # Sets active pointer position to match the current menu element
        pointer_group.x = pointer_positions[elem_index][0]
        pointer_group.y = pointer_positions[elem_index][1]

        button1_state = None

    # Page button functions
    if not button2.value and button2_state is None:  # Button stuff
        button2_state = "pressed"

    if button2.value and button2_state == "pressed":
        if screen_index != len(Screens) - 1:
            screen_index = screen_index + 1  # Increments index by 1
        elif screen_index == len(Screens) - 1:
            screen_index = 0  # Resets index to 0

        button2_state = None

    # Start/Stop functions
    if not button3.value and button3_state is None:  # Button stuff
        button3_state = "pressed"

    if button3.value and button3_state == "pressed":
        if play is True:  # Changes state to
            play = False
            play_index = 1
        else:
            play = True
            play_index = 0
        button3_state = None

    # Changes Div text to current Div
    Divtext_area.text = divisionsText[basediv]
    # Changes DivA text to current DivA
    DivAtext_area.text = divisionsText[Adiv]

    # Changes BPM text to current BPM
    BPMtext_area.text = str(beatsperminute)

    pwmsprite[0] = pw_index  # Changes PWM Sprite to the correct one
    frogesprite[0] = froge_index  # Changes froge Sprite to the correct one
    playsprite[0] = play_index

    # Makes the current screen match the screen index
    currentScreen = Screens[screen_index]

    display.show(currentScreen)  # Shows the current screen
