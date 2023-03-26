from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import board
import busio
import displayio

# ----------------------------- Screen Setup ---------------------------------#

displayio.release_displays()

spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
oled_reset = board.GP20

# Use for SPI
oled_cs = board.GP17
oled_dc = board.GP16
display_bus = displayio.FourWire(
    spi, command=oled_dc, chip_select=oled_cs, reset=oled_reset, baudrate=1000000
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

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BLACK

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Import Fonts
SMOL_FONT = bitmap_font.load_font("/Fonts/FrogPrincess-7.pcf")
BIGGE_FONT = bitmap_font.load_font("/Fonts/FrogPrincess-10.pcf")
POINTER = displayio.OnDiskBitmap("/Icons/pointer.bmp")
PLAY_SPRITE_SHEET = displayio.OnDiskBitmap("/Icons/playpause.bmp")
FROGE_SPRITE_SHEET = displayio.OnDiskBitmap("/Icons/SpinSpritesheet.bmp")
PWM_SMOL_SPRITE_SHEET = displayio.OnDiskBitmap("/Icons/PWMSpritesheetSmol.bmp")
CLOCK = displayio.OnDiskBitmap("/Icons/Clock.bmp")
# FRAME_A = displayio.OnDiskBitmap("/Icons/Frame1.bmp")


# origin is top left (0, 0)
# screen is 128x64
class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def default_formatter(value):
    return value


def div_formatter(value):
    if value >= 1:
        number = value
        char = "x"
    else:
        number = int(1 / value)
        char = "/"

    return f"{char}{number}"


class Element(displayio.Group):
    def __init__(self, name, state, coordinates, font, formatter=default_formatter):
        super().__init__()
        self.name = name
        self.state = state
        self.coordinates = coordinates
        self.formatter = formatter

        self.text_area = label.Label(
            font, color=WHITE, x=self.coordinates.x, y=self.coordinates.y // 2 - 1
        )
        self.update()
        self.append(self.text_area)

    def set_screen(self, screen):
        self.screen = screen

    def set_index(self, index):
        self.index = index

    def update(self):
        self.text_area.text = f"{self.formatter(self.state.value)}"

    def screen_type(self):
        return self.screen.screen_type()

    def get_index(self):
        return self.index


class SpriteElement(displayio.Group):
    def __init__(self, name, state, coordinates, sprite_bitmap, tile_size, scale=1):
        super().__init__()
        self.name = name
        self.state = state
        self.coordinates = coordinates

        self.sprite = displayio.TileGrid(
            sprite_bitmap,
            pixel_shader=sprite_bitmap.pixel_shader,
            width=1,
            height=1,
            tile_width=tile_size[0],
            tile_height=tile_size[1],
        )
        sprite_group = displayio.Group(scale=scale, x=coordinates.x, y=coordinates.y)
        sprite_group.append(self.sprite)
        self.append(sprite_group)

        self.update()

    def set_screen(self, screen):
        self.screen = screen

    def set_index(self, index):
        self.index = index

    def update(self):
        self.sprite[0] = int(self.state.value * 10)

    def screen_type(self):
        return self.screen.screen_type()

    def get_index(self):
        return self.index


class Pointer(displayio.Group):
    HOME_POINTER_POSITIONS = [
        Coordinates(1, 10),
        Coordinates(1, 37),
        Coordinates(1, 43),
    ]
    GATE_POINTER_POSITIONS = [
        Coordinates(50, 5),
        Coordinates(50, 25),
        Coordinates(50, 43),
    ]

    def __init__(self):
        super().__init__()
        pointer_area = displayio.TileGrid(POINTER, pixel_shader=POINTER.pixel_shader)
        self.pointer_group = displayio.Group()
        self.pointer_group.append(pointer_area)
        self.append(self.pointer_group)

    def point_to(self, focused_element):
        screen_type = focused_element.screen_type().upper()
        attr_name = f"{screen_type}_POINTER_POSITIONS"
        pointer_positions = getattr(Pointer, attr_name)
        self.pointer_group.x = pointer_positions[focused_element.get_index()].x
        self.pointer_group.y = pointer_positions[focused_element.get_index()].y


class HomeScreen(displayio.Group):
    @classmethod
    def make(cls, name, state):
        bpm_element = Element(
            "bpm",
            state.get_bpm(),
            Coordinates(20, 40),
            BIGGE_FONT,
        )

        sync_element = Element("sync", state.get_sync(), Coordinates(20, 97), SMOL_FONT)

        elements = [bpm_element, sync_element]
        screen = cls(name, elements)
        for idx, elem in enumerate(elements):
            elem.set_index(idx)
            elem.set_screen(screen)
        return screen

    def __init__(self, name, elements):
        super().__init__()
        self.name = name
        self.elements = elements
        self.froge = Froge()
        # frame_a = displayio.TileGrid(
        #    FRAME_A,
        #    pixel_shader=FRAME_A.pixel_shader,
        #    width=1,
        #    height=1,
        #    tile_width=56,
        #    tile_height=23
        # )
        # self.append(frame_a)

        self._draw_play_pause()
        self._draw_elements()
        self.append(self.froge)
        self.bpm_text_area = label.Label(
            SMOL_FONT, text="BPM", color=WHITE, x=66, y=40 // 2 - 1
        )
        self.append(self.bpm_text_area)

    def screen_type(self):
        return "home"

    def _draw_elements(self):
        [self.append(e) for e in self.elements]

    def _draw_play_pause(self):
        self.play_sprite = displayio.TileGrid(
            PLAY_SPRITE_SHEET,
            pixel_shader=PLAY_SPRITE_SHEET.pixel_shader,
            width=1,
            height=1,
            tile_width=16,
            tile_height=16,
        )
        play_sprite_group = displayio.Group(scale=1, x=55, y=35)
        play_sprite_group.append(self.play_sprite)
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
        self.frogesprite = displayio.TileGrid(
            FROGE_SPRITE_SHEET,
            pixel_shader=FROGE_SPRITE_SHEET.pixel_shader,
            width=1,
            height=1,
            tile_width=22,
            tile_height=22,
        )
        frogesprite_group = displayio.Group(scale=1, x=80, y=30)
        frogesprite_group.append(self.frogesprite)
        self.append(frogesprite_group)

    def spin(self, now, bpm):
        spin_rate = Froge.SPIN_RATE

        if not self.spinning and now >= self.prev_time + (1 / bpm) * spin_rate:
            self.prev_time = now
            self.index = (self.index + 1) % 8
            self.frogesprite[0] = self.index
            self.spinning = True

        if self.spinning and now >= self.prev_time + (1 / bpm) * spin_rate:
            self.prev_time = now
            self.index = (self.index + 1) % 8
            self.frogesprite[0] = self.index
            self.spinning = False


class GateScreen(displayio.Group):
    @classmethod
    def make(cls, name, state):
        div_element = Element(
            "div",
            state.get_div(name),
            Coordinates(90, 33),
            SMOL_FONT,
            formatter=div_formatter,
        )

        pwm_element = SpriteElement(
            "pwm",
            state.get_pwm(name),
            Coordinates(75, 20),
            PWM_SMOL_SPRITE_SHEET,
            [13, 8],
            scale=2,
        )

        elements = [div_element, pwm_element]
        screen = cls(name, elements)
        for idx, elem in enumerate(elements):
            elem.set_index(idx)
            elem.set_screen(screen)
        return screen

    def __init__(self, name, elements):
        super().__init__()
        self.name = name
        self.elements = elements
        self._draw_elements()
        self.text_area = label.Label(BIGGE_FONT, text=f"{name}", color=WHITE, x=5, y=15)
        self.append(self.text_area)

        clock = displayio.TileGrid(
            CLOCK,
            pixel_shader=CLOCK.pixel_shader,
            width=1,
            height=1,
            tile_width=15,
            tile_height=15,
            x=70,
            y=3,
        )
        self.append(clock)

    def screen_type(self):
        return "gate"

    def _draw_elements(self):
        [self.append(e) for e in self.elements]


class Screens:
    def __init__(self, state, screens):
        self.state = state
        self.screens = screens
        self.focused_screen_index = 0
        self.focused_element_index = 0
        self.screen = displayio.Group()
        self.pointer = Pointer()
        self.screen.append(self.pointer)
        self.screen.append(self.get_focused_screen())
        self._update_pointer()

    def get_focused_screen(self):
        return self.screens[self.focused_screen_index]

    def get_focused_element(self):
        return self.get_focused_screen().elements[self.focused_element_index]

    def next_screen(self):
        num_screens = len(self.screens)
        self.focused_screen_index = (self.focused_screen_index + 1) % num_screens
        self.focused_element_index = 0
        self.screen[1] = self.get_focused_screen()
        self._update_pointer()

    def next_element(self):
        num_elements = len(self.get_focused_screen().elements)
        self.focused_element_index = (self.focused_element_index + 1) % num_elements
        self._update_pointer()

    def _update_pointer(self):
        self.pointer.point_to(self.get_focused_element())

    def show_current(self):
        display.show(self.screen)
