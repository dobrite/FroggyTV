from dataclasses import dataclass

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
PLAY_SPRITE_SHEET = displayio.OnDiskBitmap("/Icons/playpause.bmp")


@dataclass
class Coordinates:
    text_x: int
    text_y: int
    label_x: int = 0
    label_y: int = 0


class Element(displayio.Group):
    def __init__(self, state, coordinates, label_text=None, color=WHITE):
        self.state = state
        self.label_text = label_text
        self.coordinates = coordinates
        self.color = color

        self.text_area = label.Label(
            BIGGE_FONT,
            text=f"{self.state.value}",
            color=self.color,
            x=self.coordinates.text_x,
            y=self.coordinates.text_y // 2 - 1
        )

        if label_text:
            self.label_text_area = label.Label(
                SMOL_FONT,
                text=self.label_text,
                color=self.color,
                x=self.coordinates.label_x,
                y=self.coordinates.label_y // 2 - 1
            )
        else:
            self.label_text_area = None

    def update(self):
        self.text_area.text = f"{self.state.value}"


class Pointer(displayio.Group):
    POINTER_POSITIONS = [[1, 5], [1, 25], [5, 43]]

    def __init__(self, focused_element):
        pointer_area = displayio.TileGrid(
            POINTER,
            pixel_shader=POINTER.pixel_shader
        )
        self.pointer_group = displayio.Group()
        self.pointer_group.append(pointer_area)

        # Pointer positions
        self.update_pointer(focused_element)
        self.append(self.pointer_group)

    def update_pointer(self, focused_element):
        self.pointer_group.x = Pointer.POINTER_POSITIONS[focused_element][0]
        self.pointer_group.y = Pointer.POINTER_POSITIONS[focused_element][1]


class HomeScreen(displayio.Group):
    @classmethod
    def make(cls, state):
        bpm_element = Element(
            state.get_bpm(),
            Coordinates(text_x=20, text_y=35, label_x=69, label_y=35),
            label_text="BPM"
        )

        div_element = Element(
            state.get_div(),
            Coordinates(text_x=28, text_y=110),
        )

        sync_element = Element(
            state.get_sync(),
            Coordinates(text_x=20, text_y=77),
        )

        elements = [bpm_element, div_element, sync_element]
        return cls(elements, state)

    def __init__(self, elements, state):
        super().__init__()
        self.elements = elements
        self._draw_play_pause()

    def _draw_play_pause(self):
        self.play_sprite = displayio.TileGrid(
            PLAY_SPRITE_SHEET,
            pixel_shader=PLAY_SPRITE_SHEET.pixel_shader,
            width=1,
            height=1,
            tile_width=16,  # Determines sprite size, Bigge tile is 41x22, Smol tile is 13x8
            tile_height=16
        )
        play_sprite_group = displayio.Group(scale=1)
        play_sprite_group.append(self.play_sprite)

        # icon positions
        play_sprite_group.x = 55
        play_sprite_group.y = 35
        self.append(play_sprite_group)

    def update_play_button(self, playing):
        self.play_sprite[0] = PLAY_ICON if playing else PAUSE_ICON


class GateScreen(displayio.Group):
    @classmethod
    def make(cls, name, state):
        div_element = Element(
            state.get_div(),  # TODO
            Coordinates(text_x=105, text_y=30, label_x=5, label_y=30),
            label_text=name,
        )

        elements = [div_element]
        return cls(elements, state)

    def __init__(self, elements, state):
        super().__init__()
        self.elements = elements


class Screens():
    def __init__(self, state, screens):
        self.state = state
        self.screens = screens
        self.pointer = Pointer(self.state.get_focused_element())

    def get_focused_screen(self):
        return self.screens[self.state.get_focused_screen()]

    def show_current(self):
        display.show(self._focused_screen_with_pointer())

    def _draw_focused_screen_with_pointer(self):
        screen = displayio.Group()
        screen.append(self.pointer)
        screen.append(self.get_focused_screen(self.state))

        return screen


# class HomeDivElement():
#     def __init__(self):
#         self.div_index = 5
#
#         mult1 = [120, "x1"]
#         mult2 = [60, "x2"]
#         mult3 = [40, "x3"]
#         mult4 = [15, "x4"]
#         mult8 = [7.5, "x8"]
#         mult16 = [3.75, "x16"]
#         div2 = [240, "/2"]
#         div3 = [360, "/3"]
#         div4 = [480, "/4"]
#         div8 = [960, "/8"]
#         div16 = [1920, "/16"]
#
#         self.divisions = [
#             div16[0],
#             div8[0],
#             div4[0],
#             div3[0],
#             div2[0],
#             mult1[0],
#             mult2[0],
#             mult3[0],
#             mult4[0],
#             mult8[0],
#             mult16[0]
#         ]
#
#         self.div_text = [
#             div16[1],
#             div8[1],
#             div4[1],
#             div3[1],
#             div2[1],
#             mult1[1],
#             mult2[1],
#             mult3[1],
#             mult4[1],
#             mult8[1],
#             mult16[1]
#         ]
