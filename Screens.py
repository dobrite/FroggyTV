import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import adafruit_displayio_ssd1306
import busio
import board

# ------------------------------- Screen Setup ------------------------------------#

displayio.release_displays()

spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
oled_reset = board.GP20

# Use for SPI
oled_cs = board.GP17
oled_dc = board.GP16
display_bus = displayio.FourWire(
    spi,
    command=oled_dc,
    chip_select=oled_cs,
    reset=oled_reset,
    baudrate=1000000
)

WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 0

PLAY_ICON = 0
PAUSE_ICON = 1

POINTER_POSITIONS = [[1, 5], [1, 25], [5, 43]]

BLACK = 0x000000
WHITE = 0xFFFFFF

display = adafruit_displayio_ssd1306.SSD1306(
    display_bus,
    width=WIDTH,
    height=HEIGHT
)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BLACK

bg_sprite = displayio.TileGrid(
    color_bitmap,
    pixel_shader=color_palette,
    x=0,
    y=0
)
splash.append(bg_sprite)

# Import Fonts
SMOL_FONT = bitmap_font.load_font("/Fonts/FrogPrincess-7.pcf")
BIGGE_FONT = bitmap_font.load_font("/Fonts/FrogPrincess-10.pcf")
POINTER = displayio.OnDiskBitmap("/Icons/pointer.bmp")


class HomeScreen(displayio.Group):
    def __init__(self, state):
        super().__init__()
        self.div = 1
        self.current_element = 0
        self.home_div_element = HomeDivElement()
        self.elements = [self.home_div_element]

        # Initial BPM text
        BPMText = f"{state.get_bpm().bpm}"
        self.BPMtext_area = label.Label(
            BIGGE_FONT,
            text=BPMText,
            color=WHITE,
            x=20,
            y=35 // 2 - 1
        )
        self.append(self.BPMtext_area)

        # Creates Label "BPM" in smaller font
        BPMLabeltext_area = label.Label(
            SMOL_FONT,
            text="BPM",
            color=WHITE,
            x=69,
            y=35 // 2 - 1
        )
        self.append(BPMLabeltext_area)

        # Creates Label "Int" in smaller font
        SyncText = f"{state.get_sync().sync}"
        self.SyncLabeltext_area = label.Label(
            SMOL_FONT,
            text=SyncText,
            color=WHITE,
            x=20,
            y=77 // 2 - 1
        )
        self.append(self.SyncLabeltext_area)

        # Initial Division text
        DivText = "x1"
        self.Divtext_area = label.Label(
            SMOL_FONT,
            text=DivText,
            color=WHITE,
            x=28,
            y=110 // 2 - 1
        )
        self.append(self.Divtext_area)

        # Draws play/pause
        playsprite_sheet = displayio.OnDiskBitmap("/Icons/playpause.bmp")
        self.playsprite = displayio.TileGrid(
            playsprite_sheet,
            pixel_shader=playsprite_sheet.pixel_shader,
            width=1,
            height=1,
            tile_width=16,  # Determines sprite size, Bigge tile is 41x22, Smol tile is 13x8
            tile_height=16
        )
        playsprite_group = displayio.Group(scale=1)
        playsprite_group.append(self.playsprite)

        # Draws the pointer icon
        pointer_area = displayio.TileGrid(
            POINTER,
            pixel_shader=POINTER.pixel_shader
        )
        self.pointer_group = displayio.Group()
        self.pointer_group.append(pointer_area)

        # Pointer positions
        self.update_pointer(state)
        self.append(self.pointer_group)

        # icon positions
        playsprite_group.x = 55
        playsprite_group.y = 35
        self.append(playsprite_group)

    def update_play_button(self, playing):
        self.playsprite[0] = PLAY_ICON if playing else PAUSE_ICON

    def get_current_element(self):
        return self.elements[self.current_element]

    def update_pointer(self, state):
        focused_element = state.get_focused_element()
        self.pointer_group.x = POINTER_POSITIONS[focused_element][0]
        self.pointer_group.y = POINTER_POSITIONS[focused_element][1]

    def update_bpm(self, state):
        self.BPMtext_area.text = f"{state.bpm}"

    def update_sync(self, state):
        self.SyncLabeltext_area.text = f"{state.sync}"


class GateScreen(displayio.Group):
    ICON_X = 5
    ICON_Y = 30
    DIV_X = 105
    DIV_Y = 30

    def __init__(self, text, state):
        super().__init__()
        self.div = 1

        # Text icon
        Labeltext_area = label.Label(
            BIGGE_FONT,
            text=text,
            color=WHITE,
            x=GateScreen.ICON_X,
            y=GateScreen.ICON_Y // 2 - 1
        )
        self.append(Labeltext_area)

        # Division text
        DivText = f"x{self.div}"
        Divtext_area = label.Label(
            SMOL_FONT,
            text=DivText,
            color=WHITE,
            x=GateScreen.DIV_X,
            y=GateScreen.DIV_Y // 2 - 1
        )
        self.append(Divtext_area)


class Screens():
    def __init__(self, state):
        self.state = state
        self.screens = [
            HomeScreen(state),
            GateScreen("A", state),
            GateScreen("B", state),
            GateScreen("C", state),
            GateScreen("D", state)
        ]

    def get_focused_screen(self):
        return self.screens[self.state.get_focused_screen()]

    def show_current(self):
        display.show(self.get_focused_screen(self.state))


class HomeDivElement():
    def __init__(self):
        self.div_index = 5

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

        self.divisions = [
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
            mult16[0]
        ]

        self.div_text = [
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
            mult16[1]
        ]
