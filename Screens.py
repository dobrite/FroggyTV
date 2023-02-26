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

SCREEN_NUMBER = 5 - 1  # Number of screens in use, may be changed later
ELEMENT_NUMBER = 3 - 1

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
FROGE_SPRITE_SHEET = displayio.OnDiskBitmap("/Icons/SpinSpritesheet.bmp")


class Coordinates:
    def __init__(self, text_x, text_y, label_x=0, label_y=0):
        self.text_x = text_x
        self.text_y = text_y
        self.label_x = label_x
        self.label_y = label_y


def default_formatter(value):
    return value


def div_formatter(value):
    if value <= 120:
        number = int(1 / (value / 120))
        char = "x"
    else:
        number = int(value / 120)
        char = "/"

    return f"{char}{number}"


class Element(displayio.Group):
    def __init__(self, state, coordinates, font, label_text=None, color=WHITE, formatter=default_formatter):
        super().__init__()
        self.state = state
        self.label_text = label_text
        self.coordinates = coordinates
        self.color = color
        self.formatter = formatter

        self.text_area = label.Label(
            font,
            text=f"{self.formatter(self.state.value)}",
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

        self.append(self.text_area)

        if self.label_text_area:
            self.append(self.label_text_area)

    def update(self):
        self.text_area.text = f"{self.formatter(self.state.value)}"


class Pointer(displayio.Group):
    HOME_POINTER_POSITIONS = [[1, 5], [1, 25], [1, 43]]
    GATE_POINTER_POSITIONS = [[50, 5], [50, 25], [50, 43]]

    def __init__(self, screen_type, focused_element):
        super().__init__()
        pointer_area = displayio.TileGrid(
            POINTER,
            pixel_shader=POINTER.pixel_shader
        )
        self.pointer_group = displayio.Group()
        self.pointer_group.append(pointer_area)

        # Pointer positions
        self.update_pointer(screen_type, focused_element)
        self.append(self.pointer_group)

    def update_pointer(self, screen_type, focused_element):
        self.pointer_group.x = getattr(Pointer, f"{screen_type}_POINTER_POSITIONS")[
            focused_element][0]
        self.pointer_group.y = getattr(Pointer, f"{screen_type}_POINTER_POSITIONS")[
            focused_element][1]

    def reset_pointer(self, screen_type):
        self.update_pointer(screen_type, 0)


class HomeScreen(displayio.Group):
    @classmethod
    def make(cls, state):
        bpm_element = Element(
            state.get_bpm(),
            Coordinates(text_x=20, text_y=35, label_x=66, label_y=35),
            BIGGE_FONT,
            label_text="BPM"
        )

        div_element = Element(
            state.get_div(),
            Coordinates(text_x=20, text_y=110),
            SMOL_FONT,
            label_text=None,
            color=WHITE,
            formatter=div_formatter,
        )

        sync_element = Element(
            state.get_sync(),
            Coordinates(text_x=20, text_y=77),
            SMOL_FONT
        )

        elements = [bpm_element, sync_element, div_element]
        return cls(elements, state)

    def __init__(self, elements, state):
        super().__init__()
        self.elements = elements
        self.froge = Froge()
        self._draw_play_pause()
        self._draw_elements()
        self.append(self.froge)

    def screen_type(self):
        return "Home"

    def _draw_elements(self):
        for e in self.elements:
            self.append(e)

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


class Froge(displayio.Group):
    SPIN_RATE = 16

    def __init__(self):
        super().__init__()
        self.spinning = False
        self.prev_time = -1
        self.index = 0
        self.frogesprite = displayio.TileGrid(FROGE_SPRITE_SHEET,
                                              pixel_shader=FROGE_SPRITE_SHEET.pixel_shader,
                                              width=1,
                                              height=1,
                                              tile_width=22,  # Determines sprite size, Bigge tile is 41x22, Smol tile is 13x8
                                              tile_height=22)
        frogesprite_group = displayio.Group(scale=1)
        frogesprite_group.append(self.frogesprite)
        # froge positions
        frogesprite_group.x = 80
        frogesprite_group.y = 30
        self.append(frogesprite_group)

    def spin(self, now, bpm):
        if not self.spinning and now >= self.prev_time + (1/bpm)*Froge.SPIN_RATE:
            self.prev_time = now
            self.index = (self.index + 1) % 8
            self.frogesprite[0] = self.index
            self.spinning = True

        if self.spinning and now >= self.prev_time + (1/bpm)*Froge.SPIN_RATE:
            self.prev_time = now
            self.index = (self.index + 1) % 8
            self.frogesprite[0] = self.index
            self.spinning = False


class GateScreen(displayio.Group):
    @classmethod
    def make(cls, name, state):
        div_element = Element(
            state.get_div(),
            Coordinates(text_x=105, text_y=30, label_x=5, label_y=30),
            SMOL_FONT,
            label_text=name,
        )

        elements = [div_element]
        return cls(elements, state)

    def __init__(self, elements, state):
        super().__init__()
        self.elements = elements
        self._draw_elements()

    def screen_type(self):
        return "Gate"

    def _draw_elements(self):
        for e in self.elements:
            self.append(e)


class Screens():
    def __init__(self, state, screens):
        self.state = state
        self.screens = screens
        self.focused_screen_index = 0
        self.focused_element_index = 0
        screen_type = self.get_focused_screen().screen_type().upper()
        self.pointer = Pointer(screen_type, self.focused_element_index)
        self.screen = displayio.Group()
        self._build_focused_screen()

    def _build_focused_screen(self):
        self.screen.append(self.pointer)
        self.screen.append(self.get_focused_screen())

    def get_focused_screen(self):
        return self.screens[self.focused_screen_index]

    def get_focused_element(self):
        return self.get_focused_screen().elements[self.focused_element_index]

    def next_screen(self):
        num_screens = len(self.screens)
        self.focused_screen_index = (
            self.focused_screen_index + 1) % num_screens
        self.screen.pop()
        self.screen.pop()
        screen_type = self.get_focused_screen().screen_type().upper()
        self.pointer.reset_pointer(screen_type)
        self._build_focused_screen()
        self.pointer.update_pointer(screen_type, self.focused_element_index)

    def next_element(self):
        num_elements = len(self.get_focused_screen().elements)
        self.focused_element_index = (
            self.focused_element_index + 1) % num_elements
        self.pointer.update_pointer(self.focused_element_index)

    def show_current(self):
        display.show(self.screen)
