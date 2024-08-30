import pygame
from pynput.keyboard import Key, Controller
import time
import pyperclip
import os
import time
from time import sleep
import sys
import json

oldDir = os.getcwd()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
sys.path.append(dname)
os.chdir(dname)
import assets as gamepad_assets

from tkinter import colorchooser
from screeninfo import get_monitors

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

RED = (255, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE = (0, 120, 215)

upper = False
keyboard = Controller()
a_string = ""
copied_glob = pyperclip.paste()
last_keystroke = time.time() - 2.0
first_copy = last_keystroke

class ControllerOverlayApp:

    def __init__(
        self, first_string, second_string, idx, idx_tmp, COLOUR_KEY, COLOUR_KEY_tmp, file_path,
        trigger_deadzone: float = 0.002,
    ):
        self.first_string, self.second_string, self.idx, self.idx_tmp, self.COLOUR_KEY, self.COLOUR_KEY_tmp = first_string, second_string, idx, idx_tmp, COLOUR_KEY, COLOUR_KEY_tmp
        self.file_path = file_path
        self.platform_map = {
            1: (gamepad_assets.Xbox1Assets, "xbox1"),
            0: (gamepad_assets.PS4Assets, "ps4"),
        }
        self.asset_map = self.platform_map[0][0]()
        gamepad_type = self.platform_map[0][1]
        self.asset_map.load()

        self.running = False
        self.window_is_framed = True
        self.trigger_deadzone = trigger_deadzone

        size = self.asset_map._base.get_size()
        self.window_size = (size[0] + 300, size[1] + 10)
        
        pygame.init()
        pygame.joystick.init()
        num_controllers = pygame.joystick.get_count()
        print(
            "Lezgo avec "
            + str(num_controllers)
            + " manette"
            + ("" if num_controllers == 1 else "s")
            + ", pour sortir du programme, appuyez sur votre stick gauche."
        )

        if num_controllers == 0:
            print(
                "Il n'y a pas de manettes mais tu peux la/les brancher maintenant 0 souss ;)"
            )
        self.BUTTON_TRANSLATION = gamepad_assets.ButtonTranslator(gamepad_type.lower())

        # Create an initial window (this will be resized)
        pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        pygame.display.set_caption("Manette Zpp")

        # Get the monitor info where the Pygame window is currently located
        self.current_monitor = get_current_monitor_info()
        self.dpi = calculate_dpi_for_monitor(self.current_monitor)
        if self.dpi is None:
            print("Could not calculate DPI for the current monitor. Using default DPI (96).")
            self.dpi = 96

        # Use the calculated DPI to determine the scaling factor
        self.base_dpi = 96  # Assume a base DPI of 96
        self.scaling_factor = self.dpi / self.base_dpi

        self.scaled_window_size = (int(self.window_size[0] * self.scaling_factor),
                            int(self.window_size[1] * self.scaling_factor))
        
        pygame.display.set_mode(self.scaled_window_size, pygame.RESIZABLE)
        self.screen = pygame.display.get_surface()
        # Define base sizes and positions for UI elements
        base_width, base_height = 200, 40
        base_x, base_y = size[0] + 20, 5

        # Scale sizes and positions according to DPI
        scaled_width = int(base_width * self.scaling_factor)
        scaled_width0 = int(280 * self.scaling_factor)
        scaled_height = int(base_height * self.scaling_factor)
        scaled_x = int(base_x * self.scaling_factor)
        scaled_y = int(base_y * self.scaling_factor)

        # Font setup
        font = pygame.font.Font(None, int(22 * self.scaling_factor))
        font0 = pygame.font.Font(None, int(20 * self.scaling_factor))

            
        # Create UI elements
        supported_gps = ("PlayStation 4", "Xbox One")
        self.line_edit0 = LineEdit(scaled_x, scaled_y, scaled_width0, scaled_height, font0, "Les deux phrases de spam qui alternent :")
        self.line_edit1 = LineEdit(scaled_x, scaled_y + scaled_height + int(20 * self.scaling_factor), scaled_width, scaled_height, font, self.first_string)
        self.line_edit2 = LineEdit(scaled_x, scaled_y + 2 * scaled_height + int(60 * self.scaling_factor), scaled_width, scaled_height, font, self.second_string)

        self.validateButton = Button(scaled_x, scaled_y + 3 * scaled_height + int(100 * self.scaling_factor), scaled_width, scaled_height, font, "Valider", self.on_button_click)

        self.colorButton = Button(scaled_x, scaled_y + 4 * scaled_height + int(140 * self.scaling_factor), scaled_width, scaled_height, font, "Couleur de font", self.get_colour)

        self.controller_dropdown = Dropdown(scaled_x, scaled_y + 5 * scaled_height + int(160 * self.scaling_factor), scaled_width, scaled_height, supported_gps, font, self.on_button_click)
    def on_button_click(self, idx0 = -1):
        if (
                (self.line_edit1.get_value() != self.line_edit2.get_value() and
                (self.line_edit1.get_value() != self.first_string or
                self.line_edit2.get_value() != self.second_string) and
                self.line_edit1.get_value() != "" and
                self.line_edit2.get_value() != ""
                )
                or
                idx0 not in [-1, self.idx] or self.COLOUR_KEY_tmp[0] != self.COLOUR_KEY[0] or
                self.COLOUR_KEY_tmp[1] != self.COLOUR_KEY[1] or self.COLOUR_KEY_tmp[2] != self.COLOUR_KEY[2]
            ):
            if idx0 not in [-1, self.idx]:
                self.idx = idx0
                assets = self.platform_map[self.idx][0]()
                gp_using = self.platform_map[self.idx][1]
                del self.asset_map
                self.asset_map = assets
                self.asset_map.load()
                gamepad_type = self.platform_map[self.idx][1]
                del self.BUTTON_TRANSLATION
                self.BUTTON_TRANSLATION = gamepad_assets.ButtonTranslator(gamepad_type.lower())
            if self.line_edit1.get_value() != self.line_edit2.get_value() and self.line_edit1.get_value() != self.first_string and self.line_edit1.get_value() != "":
                self.first_string = self.line_edit1.get_value()
            if self.line_edit1.get_value() != self.line_edit2.get_value() and self.line_edit2.get_value() != self.second_string and self.line_edit2.get_value() != "":
                self.second_string = self.line_edit2.get_value()
            if (self.COLOUR_KEY_tmp[0] != self.COLOUR_KEY[0] or
                self.COLOUR_KEY_tmp[1] != self.COLOUR_KEY[1] or self.COLOUR_KEY_tmp[2] != self.COLOUR_KEY[2]):
                self.COLOUR_KEY_tmp = self.COLOUR_KEY
            data = {
                "first_string": self.first_string,
                "second_string": self.second_string,
                "idx": self.idx,
                "R": self.COLOUR_KEY[0],
                "G": self.COLOUR_KEY[1],
                "B": self.COLOUR_KEY[2],
            }

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                print("Données des deux chaines de spam sauvegardées :)")
                
    def get_colour(self):
        col = colorchooser.askcolor(self.COLOUR_KEY)
        if col[0] != None and col[0] != self.COLOUR_KEY:
            self.COLOUR_KEY = col[0]
            self.on_button_click()

    def resize(self):
        
        # Get the monitor info where the Pygame window is currently located
        monitor = get_current_monitor_info()
        if monitor != None and self.current_monitor != monitor:
            self.current_monitor = monitor
            dpi0 = calculate_dpi_for_monitor(self.current_monitor)
            if dpi0 is None:
                print("Could not calculate DPI for the current monitor. Using default DPI (96).")
                dpi0 = 96
            if dpi != dpi0:
                self.dpi = dpi0
                # Use the calculated DPI to determine the scaling factor
                self.base_dpi = 96  # Assume a base DPI of 96
                self.scaling_factor = self.dpi / self.base_dpi

                size = self.asset_map._base.get_size()
                self.window_size = (size[0] + 300, size[1] + 10)
        
                self.scaled_window_size = (int(self.window_size[0] * self.scaling_factor),
                                    int(self.window_size[1] * self.scaling_factor))
                
                pygame.display.set_mode(self.scaled_window_size, pygame.RESIZABLE)
                self.screen = pygame.display.get_surface()
                # Define base sizes and positions for UI elements
                base_width, base_height = 200, 40
                base_x, base_y = size[0] + 15, 5

                # Scale sizes and positions according to DPI
                scaled_width = int(base_width * self.scaling_factor)
                scaled_width0 = int(280 * self.scaling_factor)
                scaled_height = int(base_height * self.scaling_factor)
                scaled_x = int(base_x * self.scaling_factor)
                scaled_y = int(base_y * self.scaling_factor)

                # Font setup
                font = pygame.font.Font(None, int(22 * self.scaling_factor))
                font0 = pygame.font.Font(None, int(22 * self.scaling_factor))

                # resize UI elements
                self.line_edit0.resize(scaled_x, scaled_y, scaled_width0, scaled_height)
                self.line_edit1.resize(scaled_x, scaled_y + scaled_height + int(20 * self.scaling_factor), scaled_width, scaled_height)
                self.line_edit2.resize(scaled_x, scaled_y + 2 * scaled_height + int(60 * self.scaling_factor), scaled_width, scaled_height)

                self.validateButton.resize(scaled_x, scaled_y + 3 * scaled_height + int(100 * self.scaling_factor), scaled_width, scaled_height)

                self.colorButton.resize(scaled_x, scaled_y + 4 * scaled_height + int(140 * self.scaling_factor), scaled_width, scaled_height)
                self.controller_dropdown.resize(scaled_x, scaled_y + 5 * scaled_height + int(160 * self.scaling_factor), scaled_width, scaled_height)

        
    def run(self):
        joysticks = {}
        self.running = True 
        while self.running:
            self.resize()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (
                        event.button == 3
                    ):  # right click to make frame available, so we can move the window around easily
                        if not self.window_is_framed:
                            self.window_is_framed = True
                            self.screen = pygame.display.set_mode(self.scaled_window_size)
                        else:
                            self.window_is_framed = False
                            self.screen = pygame.display.set_mode(
                                self.scaled_window_size, pygame.NOFRAME
                            )

                if event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks[joy.get_instance_id()] = joy
                    print(f"Manette {joy.get_name()} {joy.get_instance_id()} connecté")

                if (
                    event.type == pygame.JOYDEVICEREMOVED
                    and event.instance_id in joysticks
                ):
                    print(
                        f"Manette {joysticks[event.instance_id].get_name()} {event.instance_id} déconnecté"
                    )
                    del joysticks[event.instance_id]
                self.controller_dropdown.handle_event(event)
                self.line_edit1.handle_event(event)
                self.line_edit2.handle_event(event)
                if(self.line_edit1.get_value() != self.line_edit2.get_value() and
                    (self.line_edit1.get_value() != self.first_string or
                    self.line_edit2.get_value() != self.second_string) and
                self.line_edit1.get_value() != "" and
                self.line_edit2.get_value() != "" 
                ):
                    self.validateButton.handle_event(event)
            
                self.colorButton.handle_event(event)
            
            self.screen.fill(self.COLOUR_KEY)
            self.screen.blit(self.asset_map._base, (5, 5))

            self.controller_dropdown.draw(self.screen)
            self.line_edit0.draw(self.screen)
            self.line_edit1.draw(self.screen)
            self.line_edit2.draw(self.screen)
            if(self.line_edit1.get_value() != self.line_edit2.get_value() and
                (self.line_edit1.get_value() != self.first_string or
                self.line_edit2.get_value() != self.second_string) and
                self.line_edit1.get_value() != "" and
                self.line_edit2.get_value() != ""
            ):
                self.validateButton.draw(self.screen)
            
            self.colorButton.draw(self.screen)
            
            for joystick in joysticks.values():
                current_controller_type = ""
                if (
                    "xbox" in joystick.get_name().lower()
                    or "ultimate" in joystick.get_name().lower()
                ):
                    current_controller_type = "xbox1"
                else:
                    current_controller_type = "ps4"
                num_tmp = 0
                if joystick.get_button(0) == 1:
                    type_word("a")

                if joystick.get_button(1) == 1:
                    type_word("b")

                if current_controller_type == "xbox1":
                    num_tmp = joystick.get_button(5)
                else:
                    num_tmp = joystick.get_button(10)

                if num_tmp == 1:
                    type_paste(self.first_string, self.second_string)

                if joystick.get_button(11) == 1:
                    type_word("haut")

                if joystick.get_button(12) == 1:
                    type_word("bas")

                if joystick.get_button(13) == 1:
                    type_word("droite")

                if joystick.get_button(14) == 1:
                    type_word("gauche")

                need_to_quit = 0
                if current_controller_type == "xbox1":
                    need_to_quit = joystick.get_button(8)
                else:
                    need_to_quit = joystick.get_button(7)

                if need_to_quit == 1:
                    self.running = False
                    break

                for hat_num in range(joystick.get_numhats()):
                    hat = joystick.get_hat(hat_num)

                    if hat[1] == 1:
                        type_word("haut")

                    if hat[1] == -1:
                        type_word("bas")

                    if hat[0] == 1:
                        type_word("droite")

                    if hat[0] == -1:
                        type_word("gauche")

                axes = joystick.get_numaxes()

                if axes >= 2:
                    x = joystick.get_axis(0)
                    y = joystick.get_axis(1)
                    if y >= 0.5 and x < 0.5 and x > -0.5:
                        type_word("bas")
                    elif y <= -0.5 and x < 0.5 and x > -0.5:
                        type_word("haut")
                    elif x <= -0.5 and y < 0.5 and y > -0.5:
                        type_word("gauche")
                    elif x >= 0.5 and y < 0.5 and y > -0.5:
                        type_word("droite")

                if axes >= 4:
                    x = joystick.get_axis(2)
                    y = joystick.get_axis(3)
                    if y >= 0.5 and x < 0.5 and x > -0.5:
                        type_word("bas")
                    elif y <= -0.5 and x < 0.5 and x > -0.5:
                        type_word("haut")
                    elif x <= -0.5 and y < 0.5 and y > -0.5:
                        type_word("gauche")
                    elif x >= 0.5 and y < 0.5 and y > -0.5:
                        type_word("droite")
                
                for button_num in range(joystick.get_numbuttons()):
                    button_is_pressed = joystick.get_button(button_num)
                    button_ID = self.BUTTON_TRANSLATION(button_num, current_controller_type)
                    if button_ID in self.asset_map.analogs and not button_is_pressed:
                        if button_ID == self.asset_map.left_analog:
                            left_analog = self.asset_map[button_ID][button_is_pressed]
                        else:
                            right_analog = self.asset_map[button_ID][button_is_pressed]
                    elif button_ID in self.asset_map.analogs and button_is_pressed:
                        if button_ID == self.asset_map.left_analog:
                            left_analog = self.asset_map[button_ID][button_is_pressed]
                        else:
                            right_analog = self.asset_map[button_ID][button_is_pressed]
                    elif button_ID not in self.asset_map.analogs:
                        try:
                            btndat = self.asset_map[button_ID][button_is_pressed]
                            self.screen.blit(btndat["img"], btndat["loc"])
                        except (KeyError, TypeError):
                            continue

                dpad_state = joystick.get_hat(0)
                for im, loc in self.asset_map[dpad_state]:
                    self.screen.blit(im, loc)

                # Analog Stick movement
                left_ana_horiz, left_ana_verti = round(
                    joystick.get_axis(
                        self.BUTTON_TRANSLATION(self.asset_map.left_stick_x, current_controller_type)
                    ),
                    2,
                ), round(
                    joystick.get_axis(
                        self.BUTTON_TRANSLATION(self.asset_map.left_stick_y, current_controller_type)
                    ),
                    2,
                )
                right_ana_horiz, right_ana_verti = round(
                    joystick.get_axis(
                        self.BUTTON_TRANSLATION(self.asset_map.right_stick_x, current_controller_type)
                    ),
                    2,
                ), round(
                    joystick.get_axis(
                        self.BUTTON_TRANSLATION(self.asset_map.right_stick_y, current_controller_type)
                    ),
                    2,
                )

                self.screen.blit(
                    left_analog["img"],
                    (
                        left_analog["loc"][0] + (30 * left_ana_horiz),
                        left_analog["loc"][1] + (30 * left_ana_verti),
                    ),
                )
                self.screen.blit(
                    right_analog["img"],
                    (
                        right_analog["loc"][0] + (30 * right_ana_horiz),
                        right_analog["loc"][1] + (30 * right_ana_verti),
                    ),
                )

                if axes >= 6:
                    lt = self.asset_map.left_trigger
                    rt = self.asset_map.right_trigger
                    if max(0, (joystick.get_axis(4) + 1) / 2) > self.trigger_deadzone:
                        self.screen.blit(lt['img'], lt['loc'])
                    if max(0, (joystick.get_axis(5) + 1) / 2) > self.trigger_deadzone:
                        self.screen.blit(rt['img'], rt['loc'])
                pygame.display.update()


# Class for the Dropdown widget
class Dropdown:
    def __init__(self, x, y, w, h, options, font, callback, default_option=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.selected_option = options[default_option] if default_option < len(options) else options[0]
        self.font = font
        self.active = False
        self.hovered = False
        self.callback = callback

    def resize(self, x, y, w, h):
        self.rect.x = x
        self.rect.y = y
        self.rect.width = w
        self.rect.height = h

    def draw(self, screen):
        global WHITE, BLACK, GRAY, LIGHT_GRAY, BLUE
        pygame.draw.rect(screen, LIGHT_GRAY if self.hovered else WHITE, self.rect, 0)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text = self.font.render(self.selected_option, True, BLACK)
        screen.blit(text, (self.rect.x + 10, self.rect.y + 10))

        if self.active:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y + (i + 1) * self.rect.height,
                    self.rect.width,
                    self.rect.height,
                )
                pygame.draw.rect(
                    screen, GRAY if i % 2 == 0 else LIGHT_GRAY, option_rect, 0
                )
                pygame.draw.rect(screen, BLACK, option_rect, 1)
                option_text = self.font.render(option, True, BLACK)
                screen.blit(option_text, (option_rect.x + 10, option_rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            elif self.active:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.y + (i + 1) * self.rect.height,
                        self.rect.width,
                        self.rect.height,
                    )
                    if option_rect.collidepoint(event.pos):
                        self.selected_option = option
                        self.callback(i)
                        self.active = False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

    def get_value(self):
        return self.selected_option


# Class for the LineEdit widget
class LineEdit:
    def __init__(self, x, y, w, h, font, text=""):
        global WHITE, BLACK, GRAY, LIGHT_GRAY, BLUE
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = text
        self.active = False
        self.color = GRAY

    def resize(self, x, y, w, h):
        self.rect.x = x
        self.rect.y = y
        self.rect.width = w
        self.rect.height = h
        
    def draw(self, screen):
        global WHITE, BLACK, GRAY, LIGHT_GRAY, BLUE
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        global WHITE, BLACK, GRAY, LIGHT_GRAY, BLUE
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = BLUE
            else:
                self.active = False
                self.color = GRAY
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def get_value(self):
        return self.text


# Class for the Button widget
class Button:
    def __init__(self, x, y, w, h, font, text, callback):
        global WHITE, BLACK, GRAY, LIGHT_GRAY, BLUE
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = text
        self.callback = callback
        self.color = GRAY
        self.hovered = False
        
    def resize(self, x, y, w, h):
        self.rect.x = x
        self.rect.y = y
        self.rect.width = w
        self.rect.height = h
        
    def draw(self, screen):
        global WHITE, BLACK, GRAY, LIGHT_GRAY, BLUE
        pygame.draw.rect(screen, self.color if self.hovered else LIGHT_GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(
            text_surface,
            (
                self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                self.rect.y + (self.rect.height - text_surface.get_height()) // 2,
            ),
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)


# Function to get current monitor info
def get_current_monitor_info():
    window_pos = pygame.display.get_window_position()
    monitors = get_monitors()
    for monitor in monitors:
        if (
            monitor.x <= window_pos[0] < monitor.x + monitor.width
            and monitor.y <= window_pos[1] < monitor.y + monitor.height
        ):
            return monitor
    return None


# Function to calculate DPI for the current monitor
def calculate_dpi_for_monitor(monitor):
    if monitor != None and monitor.width_mm != None and monitor.height_mm != None and monitor.width != None and monitor.height != None:
        if monitor.width_mm > 0 and monitor.height_mm > 0 and monitor.width > 0 and monitor.height > 0:
            width_in_inches = monitor.width_mm / 25.4
            height_in_inches = monitor.height_mm / 25.4
            if width_in_inches > 0 and height_in_inches > 0:
                dpi_x = monitor.width / width_in_inches
                dpi_y = monitor.height / height_in_inches
                dpi = (dpi_x + dpi_y) / 2
                return dpi
    return None


def type_word(word):
    global last_keystroke, upper

    now = time.time()

    if (now - last_keystroke) > 1.5:
        last_keystroke = now
        output = ""
        if upper:
            output = word.upper()
        else:
            output = word

        print(output)

        write_to_cursor(output)

        upper = not upper


def type_paste(first_string, second_string):
    global a_string, copied_glob, last_keystroke, first_copy
    now = time.time()
    if (now - last_keystroke) > 1.5:
        last_keystroke = now
        copied = pyperclip.paste()
        if copied[: len(copied_glob)] == copied_glob:
            if (now - first_copy) > 30:
                first_copy = now
                pyperclip.copy(copied_glob)
                a_string = first_string
            else:
                pyperclip.copy(copied + " " + a_string)
                if a_string == first_string:
                    a_string = second_string
                else:
                    a_string = first_string
        else:
            first_copy = now
            copied_glob = copied
            pyperclip.copy(copied)
            a_string = first_string

        print(pyperclip.paste())
        press_combined_key(Key.ctrl, "a")
        press_combined_key(Key.ctrl, "v")
        press_key(Key.enter)


def write_to_cursor(word):
    press_combined_key(Key.ctrl, "a")
    for char in word:
        press_key(char)
    press_key(Key.enter)

def press_key(character):
    keyboard.press(character)
    time.sleep(0.001)
    keyboard.release(character)
    time.sleep(0.001)


def press_combined_key(character1, character2):
    keyboard.press(character1)
    keyboard.press(character2)
    time.sleep(0.001)
    keyboard.release(character2)
    keyboard.release(character1)
    time.sleep(0.001)


def main():
    COLOUR_KEY = (150, 150, 150)  # gray

    first_string = "o"
    second_string = "k"
    idx = 0
    
    # File path
    file_path = ".zppControllerToChatV2Save.json"

    # Step 1: Check if the file exists
    if os.path.exists(file_path):
        # Step 2: Read and parse the JSON file with UTF-8 encoding
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if (
                    "first_string" in data and "second_string" in data and
                    "idx" in data and "R" in data and "G" in data and "B" in data
                    ):
                    first_string = str(data["first_string"])
                    second_string = str(data["second_string"])
                    idx = int(data["idx"])
                    r = int(data["R"])
                    g = int(data["G"])
                    b = int(data["B"])
                    COLOUR_KEY = (r, g, b)
                    print("Données des deux chaines de spam récupérées :)")
            except json.JSONDecodeError:
                print("Error: File content is not valid JSON.")

    idx_tmp = idx
    COLOUR_KEY_tmp = COLOUR_KEY

    app = ControllerOverlayApp(first_string, second_string, idx, idx_tmp, COLOUR_KEY, COLOUR_KEY_tmp, file_path)
    app.run()
    pygame.quit()
            


if __name__ == "__main__":
    main()
