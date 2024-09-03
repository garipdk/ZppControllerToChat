import pygame
from pynput.keyboard import Key, Controller
import time
import pyperclip
import os
import time
from time import sleep
import sys
import json
from pathlib import Path

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
BLACKRED = (127, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE = (0, 120, 215)
GREEN = (40, 200, 70)

upper = False
keyboard = Controller()
a_string = ""
copied_glob = pyperclip.paste()
last_keystroke = time.time() - 2.0
first_copy = last_keystroke

MUSIC_END = pygame.USEREVENT+1

class ControllerOverlayApp:

    def __init__(
        self, first_string, second_string, idx, idx_tmp, COLOUR_KEY, COLOUR_KEY_tmp, file_path, delais, delais_tmp,
        trigger_deadzone: float = 0.002,
    ):
        self.first_string, self.second_string, self.idx, self.idx_tmp, self.COLOUR_KEY, self.COLOUR_KEY_tmp = first_string, second_string, idx, idx_tmp, COLOUR_KEY, COLOUR_KEY_tmp
        if self.idx < 0 or self.idx > 1:
            self.idx = 0
        self.file_path = file_path
        self.platform_map = {
            0: (gamepad_assets.PS4Assets, "ps4"),
            1: (gamepad_assets.Xbox1Assets, "xbox1"),
        }
        self.asset_map = self.platform_map[self.idx][0]()
        gamepad_type = self.platform_map[self.idx][1]
        self.asset_map.load()

        self.running = False
        self.window_is_framed = True
        self.trigger_deadzone = trigger_deadzone
        
        sizeX = pygame.image.load(str(Path(__file__).parent / "main_assets" / "ps4" / "pngs" / "controller_base.png")).get_size()
        sizeY = pygame.image.load(str(Path(__file__).parent / "main_assets" / "xbox1" / "pngs" / "controller_base.png")).get_size()
        size = (sizeX[0], sizeY[1])
        self.window_size = (size[0] + 300, size[1] + 10)
        
        self.delais = delais
        self.delais_tmp = delais_tmp

        self.ibeam_cursor_needed = []
        self.hand_cursor_needed = []



        ### KONAMI_CODE

        pygame.mixer.init(44100,-16,2, 1024)
        pygame.mixer.music.set_endevent(MUSIC_END)

        self.code = ["haut","haut","bas","bas","gauche","droite","gauche","droite","b","a", "start"]
        self.code_last_keystroke = ''
        self.code_idx = 0
        self.code_image = pygame.image.load(str(Path(__file__).parent / "main_assets" / "by_ShinyCyan.png"))
        self.code_sound = pygame.mixer.music.load((str(Path(__file__).parent / "main_assets" / "flopEvent.ogg")))

        ### KONAMI_CODE // END

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
        pygame.display.set_mode(self.window_size, pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption("Manette Zpp")
        
        self.screen = pygame.display.get_surface()
        # Define base sizes and positions for UI elements
        base_width, base_height = 200, 40
        base_x, base_y = size[0] + 20, 5
        base_width0 = 280

        # Font setup
        font = pygame.font.Font(None, int(22))
        font0 = pygame.font.Font(None, int(20))
        font1 = pygame.font.Font(None, int(42))

        self.close_button = Button(self.window_size[0] - 30 - 10, 10, 30, 30 , font1, "x", pygame.mixer.music.stop, base_color=RED, hover_color=BLACKRED)
         
        # Create UI elements
        supported_gps = ("PlayStation 4", "Xbox One")
        self.line_edit0 = LineEdit(base_x - 30, base_y, base_width0, base_height, font, "Les deux phrases de spam qui alternent :", False)
        self.line_edit1 = LineEdit(base_x, base_y + base_height + int(0), base_width, base_height, font, self.first_string)
        self.ibeam_cursor_needed.append(self.line_edit1)
        self.line_edit2 = LineEdit(base_x, base_y + 2 * base_height + int(10), base_width, base_height, font, self.second_string)
        self.ibeam_cursor_needed.append(self.line_edit2)


        self.validateButton = Button(base_x, base_y + 3 * base_height + int(20), base_width, base_height, font, "Valider", self.save_to_json, hover_color=GREEN)

        self.colorButton = Button(base_x, base_y + 4 * base_height + int(40), base_width, base_height, font, "Couleur de fond", self.get_colour, hover_color=BLUE)

        self.controller_dropdown = Dropdown(base_x, base_y + 5 * base_height + int(60), base_width, base_height, supported_gps, font, self.save_to_json, self.idx)
        self.hand_cursor_needed.append(self.controller_dropdown)

        self.line_edit4 = LineEdit(base_x, base_y + 6 * base_height + int(80), base_width, base_height, font, "Delais : ", False)
        self.line_edit3 = LineEdit(base_x + 50, base_y + 7 * base_height + int(80), 50, base_height, font, f"{self.delais:.2f} s")
        self.btn_add = Button(base_x + 45 + 5 + 50 + 5, base_y + 7 * base_height + int(80), 45, base_height, font, "+", self.add_delais)
        self.btn_sub = Button(base_x, base_y + 7 * base_height + int(80), 45, base_height, font, "-", self.sub_delais)

        self.radio_button_box = RadioButtonBox(base_x, base_y + 8 * base_height + int(100), self.screen.width - base_x - 10, 60, font, "Réglage avancé du delais", ["0.10s", "0.20s", "0.50s", "1s", "2s", "5s"], selected_option=2, button_font=font0)

    def add_delais(self):
        # recupper le bouton radio pour savoir quoi ajouter
        new_delais = self.delais + float(self.radio_button_box.get_value()[:-1])
        self.update_and_save_delais(new_delais)

    def sub_delais(self):
        new_delais = self.delais - float(self.radio_button_box.get_value()[:-1])
        new_delais = max(0, new_delais)
        # recupper le bouton radio pour savoir quoi ajouter
        self.update_and_save_delais(new_delais)

    def update_and_save_delais(self, new_delais: float):
        self.delais = new_delais
        self.line_edit3.set_value(f"{new_delais:.2f} s")
        self.save_to_json()


    def save_to_json(self, idx0 = -1):
        if (
                (self.line_edit1.get_value() != self.line_edit2.get_value() and
                (self.line_edit1.get_value() != self.first_string or
                self.line_edit2.get_value() != self.second_string) and
                self.line_edit1.get_value() != "" and
                self.line_edit2.get_value() != ""
                )
                or
                idx0 not in [-1, self.idx] or self.COLOUR_KEY_tmp[0] != self.COLOUR_KEY[0] or
                self.COLOUR_KEY_tmp[1] != self.COLOUR_KEY[1] or self.COLOUR_KEY_tmp[2] != self.COLOUR_KEY[2] or
                self.delais_tmp != self.delais
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
            if self.delais_tmp != self.delais:
                self.delais_tmp = self.delais
            data = {
                "first_string": self.first_string,
                "second_string": self.second_string,
                "idx": self.idx,
                "R": self.COLOUR_KEY[0],
                "G": self.COLOUR_KEY[1],
                "B": self.COLOUR_KEY[2],
                "delais" : self.delais,
            }

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                print("Données sauvegardées :)")
                
    def get_colour(self):
        col = colorchooser.askcolor(self.COLOUR_KEY)
        if col[0] != None and col[0] != self.COLOUR_KEY:
            self.COLOUR_KEY = col[0]
            self.save_to_json()

    def run(self):
        joysticks = {}
        self.running = True
        while self.running:
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
                            self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE | pygame.SCALED)
                        else:
                            self.window_is_framed = False
                            self.screen = pygame.display.set_mode(
                                self.window_size, pygame.RESIZABLE | pygame.SCALED | pygame.NOFRAME
                            )
                elif event.type == pygame.MOUSEMOTION:
                    special_cursor_needed = 0
                    for le in self.ibeam_cursor_needed:
                        if le.rect.collidepoint(event.pos):
                            special_cursor_needed = 1
                            break
                        
                    for h in self.hand_cursor_needed:
                        if h.rect.collidepoint(event.pos):
                            special_cursor_needed = 2
                            break

                    match special_cursor_needed:
                        case 1:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                        case 2:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        case _:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

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
                self.btn_sub.handle_event(event)
                self.btn_add.handle_event(event)
                if(self.line_edit1.get_value() != self.line_edit2.get_value() and
                    (self.line_edit1.get_value() != self.first_string or
                    self.line_edit2.get_value() != self.second_string) and
                self.line_edit1.get_value() != "" and
                self.line_edit2.get_value() != "" 
                ):
                    self.validateButton.handle_event(event)
            
                self.colorButton.handle_event(event)
                self.radio_button_box.handle_event(event)
                self.close_button.handle_event(event)
            
            self.screen.fill(self.COLOUR_KEY)
            self.screen.blit(self.asset_map._base, (5, 5))

            self.line_edit0.draw(self.screen)
            self.line_edit1.draw(self.screen)
            self.line_edit2.draw(self.screen)
            self.line_edit4.draw(self.screen)
            self.line_edit3.draw(self.screen)
            self.btn_sub.draw(self.screen)
            self.btn_add.draw(self.screen)
            self.radio_button_box.draw(self.screen)
            self.controller_dropdown.draw(self.screen)

            if(self.line_edit1.get_value() != self.line_edit2.get_value() and
                (self.line_edit1.get_value() != self.first_string or
                self.line_edit2.get_value() != self.second_string) and
                self.line_edit1.get_value() != "" and
                self.line_edit2.get_value() != ""
            ):
                self.validateButton.draw(self.screen)
            
            self.colorButton.draw(self.screen)
            
            TMP_last = ""

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
                    type_word("a", self.delais)
                    TMP_last = "a"

                if joystick.get_button(1) == 1:
                    type_word("b", self.delais)
                    TMP_last = "b"

                if joystick.get_button(2) == 1:
                    type_word("x", self.delais)
                    TMP_last = "x"

                if joystick.get_button(3) == 1:
                    type_word("y", self.delais)
                    TMP_last = "y"

                if current_controller_type == "xbox1":
                    num_tmp = joystick.get_button(5)
                else:
                    num_tmp = joystick.get_button(10)

                if num_tmp == 1:
                    type_paste(self.first_string, self.second_string, self.delais)

                if current_controller_type != "xbox1":
                    if joystick.get_button(11) == 1:
                        type_word("haut", self.delais)
                        TMP_last = "haut"

                    if joystick.get_button(12) == 1:
                        type_word("bas", self.delais)
                        TMP_last = "bas"

                    if joystick.get_button(13) == 1:
                        type_word("gauche", self.delais)
                        TMP_last = "gauche"

                    if joystick.get_button(14) == 1:
                        type_word("droite", self.delais)
                        TMP_last = "droite"

                num_tmp = 0
                if current_controller_type == "xbox1":
                    num_tmp = joystick.get_button(7)
                else:
                    num_tmp = joystick.get_button(6)

                if num_tmp == 1:
                    type_word("start", self.delais)
                    TMP_last = "start"

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
                        type_word("haut", self.delais)
                        TMP_last = "haut"

                    if hat[1] == -1:
                        type_word("bas", self.delais)
                        TMP_last = "bas"

                    if hat[0] == 1:
                        type_word("droite", self.delais)
                        TMP_last = "droite"

                    if hat[0] == -1:
                        type_word("gauche", self.delais)
                        TMP_last = "gauche"

                axes = joystick.get_numaxes()

                if axes >= 2:
                    x = joystick.get_axis(0)
                    y = joystick.get_axis(1)
                    if y >= 0.5 and x < 0.5 and x > -0.5:
                        type_word("bas", self.delais)
                        TMP_last = "bas"
                    elif y <= -0.5 and x < 0.5 and x > -0.5:
                        type_word("haut", self.delais)
                        TMP_last = "haut"
                    elif x <= -0.5 and y < 0.5 and y > -0.5:
                        type_word("gauche", self.delais)
                        TMP_last = "gauche"
                    elif x >= 0.5 and y < 0.5 and y > -0.5:
                        type_word("droite", self.delais)
                        TMP_last = "droite"

                if axes >= 4:
                    x = joystick.get_axis(2)
                    y = joystick.get_axis(3)
                    if y >= 0.5 and x < 0.5 and x > -0.5:
                        type_word("bas", self.delais)
                        TMP_last = "bas"
                    elif y <= -0.5 and x < 0.5 and x > -0.5:
                        type_word("haut", self.delais)
                        TMP_last = "haut"
                    elif x <= -0.5 and y < 0.5 and y > -0.5:
                        type_word("gauche", self.delais)
                        TMP_last = "gauche"
                    elif x >= 0.5 and y < 0.5 and y > -0.5:
                        type_word("droite", self.delais)
                        TMP_last = "droite"
                
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
                            self.screen.blit(btndat["img"],btndat["loc"])
                        except (KeyError, TypeError):
                            continue
                for i in range(joystick.get_numhats()):
                    dpad_state = joystick.get_hat(i)
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


                ### KONAMI_CODE
                if (TMP_last != self.code_last_keystroke):
                    self.code_last_keystroke = TMP_last
                    if self.code_last_keystroke != '' and self.code_last_keystroke == self.code[self.code_idx]:
                        self.code_idx += 1
                        if (self.code_idx>= len(self.code)):
                            pygame.mixer.music.play()
                            self.code_idx = 0
                    elif self.code_last_keystroke != '':
                        self.code_idx = 0

                if pygame.mixer.music.get_busy():
                    self.screen.fill((0x18, 0x18, 0x18))
                    self.screen.blit(self.code_image, ((self.screen.width / 2) - (self.code_image.width / 2), 10))
                    font = pygame.font.Font(None, int(22))
                    self.text_surface = font.render("Pixel art by ShinyCyan 2022", True, WHITE)
                    self.screen.blit(self.text_surface, ((self.screen.width / 2) - (self.code_image.width / 2), 10 + self.code_image.height + 10))
                    self.close_button.draw(self.screen)
                ### KONAMI_CODE // END


                pygame.display.update()


# Class for the Dropdown widget
class Dropdown:
    def __init__(self, x, y, w, h, options, font, callback, default_option=0, base_color=LIGHT_GRAY, hover_color=WHITE):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.selected_option = options[default_option] if default_option < len(options) else options[0]
        self.font = font
        self.active = False
        self.hovered = False
        self.callback = callback
        self.base_color = base_color
        self.hover_color = hover_color

    def draw(self, screen):
        global WHITE, BLACK, GRAY, LIGHT_GRAY, BLUE
        pygame.draw.rect(screen, self.base_color if self.hovered else self.hover_color, self.rect, 0)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # dessiner un carée pour y mettre le future triangle
        pygame.draw.rect(screen, BLACK, pygame.Rect(self.rect.right - self.rect.height, self.rect.top, self.rect.height, self.rect.height), 2)

        # points pour faire un triangle vers le bas
        downward_triangle = []
        downward_triangle.append((self.rect.right - self.rect.height + 12, self.rect.top + 12))
        downward_triangle.append((self.rect.right - 12, self.rect.top + 12))
        downward_triangle.append((self.rect.right - self.rect.height + 12 + ((self.rect.right - 12) - (self.rect.right - self.rect.height + 12)) * 0.5, self.rect.bottom - 12))

        # points pour faire un triangle vers le haut
        upward_triangle = []
        upward_triangle.append((self.rect.right - self.rect.height + 12, self.rect.bottom - 12))
        upward_triangle.append((self.rect.right - 12, self.rect.bottom - 12))
        upward_triangle.append((self.rect.right - self.rect.height + 12 + ((self.rect.right - 12) - (self.rect.right - self.rect.height + 12)) * 0.5, self.rect.top + 12))

        # dessiner le bon triangle
        pygame.draw.aalines(screen, BLACK, True, upward_triangle if self.active else downward_triangle)

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
    def __init__(self, x, y, w, h, font, text="", border=True):
        global WHITE, BLACK, GRAY, LIGHT_GRAY, BLUE
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = text
        self.active = False
        self.color = GRAY
        self.border = border

        self.text_surface = self.font.render(self.text, True, BLACK)
        self.text_rect = self.text_surface.get_rect()
        self.cursor = pygame.Rect(self.text_rect.topright, (3, self.text_rect.height + 2))
        
    def draw(self, screen):
        global WHITE, BLACK, GRAY, LIGHT_GRAY, BLUE
        self.text_surface = self.font.render(self.text, True, BLACK)
        if self.border:
            pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.text_surface, (self.rect.x + (5 if self.border else 0), self.rect.y + (self.rect.height / 2) - (self.text_surface.get_height() / 2) + 2 ))
        if self.active and time.time() % 1 > 0.5:
           # bounding rectangle of the text
            text_rect = self.text_surface.get_rect(topleft = (self.rect.x + 5, self.rect.y + 10))
            # set cursor position
            self.cursor.midleft = text_rect.midright
            pygame.draw.rect(screen, self.color, self.cursor)

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

    def set_value(self, text : str):
        self.text = text

# Class for the Button widget
class Button:
    def __init__(self, x, y, w, h, font, text, callback, callback_args:list[str] = None, base_color=LIGHT_GRAY, hover_color=GRAY):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = text
        self.callback = callback
        self.base_color = base_color
        self.hover_color = hover_color
        self.hovered = False
        self.callback_args = callback_args
        
    def draw(self, screen):
        global WHITE, BLACK, GRAY, LIGHT_GRAY, BLUE
        pygame.draw.rect(screen, self.hover_color if self.hovered else self.base_color, self.rect)
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
                if self.callback_args:
                    self.callback(''.join(self.callback_args))
                else:
                    self.callback()
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

    def set_base_color(self, color):
        self.base_color = color
    
    def set_hover_color(self, color):
        self.hover_color = color


# Class for the CheckBox widget
class CheckBox:

    def __init__(self, x, y, w, h, font=None, text=None, checked=False):
        global  GRAY
        self.rect = pygame.Rect(x, y, w, h)
        self.active = False
        self.color = GRAY
        self.checked = checked
        self.font = font
        self.text = text
        self.text_surface = None

        if self.font and self.text:
            self.text_surface = self.font.render(self.text, True, BLACK)

    def draw(self, screen):
        global BLACK

        # SECTION CheckBox
        pygame.draw.rect(screen, self.color, self.rect, 2)

        if self.checked:
            icon = pygame.image.load(str(Path(__file__).parent / "main_assets" / "check-mark-icon.png"))
            
            offset = 0.2
            check_mark_offset = (self.rect.width * offset, self.rect.height * offset)
            check_icon_size = (self.rect.width + check_mark_offset[0], self.rect.height + check_mark_offset[1])
            check_icon = pygame.transform.scale(icon, check_icon_size)
            check_icon_position = ( self.rect.x - check_mark_offset[0] / 2, self.rect.y - check_mark_offset[1])

            screen.blit(check_icon, check_icon_position)

        # SECTION Label
        if self.text_surface:
            screen.blit(self.text_surface, (self.rect.x + self.rect.width + 5, self.rect.y + (self.rect.height / 2) - (self.text_surface.get_height() / 2) + 2 ))


    def handle_event(self, event):
        global  GRAY, BLUE

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked

        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = BLUE
            else:
                self.active = False
                self.color = GRAY

    def get_checked(self):
        return self.checked

    def get_size(self):
        return ( self.rect.width + 5 + (self.text_surface.width if self.text_surface else 0), self.rect.height)


# Class for the RadioButtonBox widget
class RadioButtonBox:

    def __init__(self, x, y, w, h, font, text, labels: list[str], maximized=False, padding=5, button_font=None, selected_option=0):
        global  GRAY
        self.rect = pygame.Rect(x, y, w, h)
        self.active = False
        self.color = GRAY
        self.font = font
        self.text = text
        self.buttons = []
        self.maximized = maximized
        self.checkbox = CheckBox(self.rect.x + 10 * 1.5, self.rect.y - 10 , 20, 20, font, self.text, maximized)
        self.labels = labels
        self.padding = 5
        self.button_font = button_font if button_font else font
        self.selected_option = selected_option
        
        self.item_count = len(self.labels)
        padding_count = self.item_count + 1
        button_width = (self.rect.width - (padding * padding_count)) // self.item_count

        for i in range(0, self.item_count):
            xx = self.rect.x + (i+ 1) * padding + (i * button_width) 
            yy = self.rect.y + padding + (self.checkbox.rect.height / 2)
            btn = Button(xx, yy, button_width, self.rect.height - 2*padding - (self.checkbox.rect.height / 2), self.button_font, self.labels[i], self.button_click, callback_args=[str(i)], base_color=LIGHT_GRAY, hover_color=BLUE)
            self.buttons.append(btn)

    def draw(self, screen):

        self.maximized = self.checkbox.checked
        self.checkbox.draw(screen)

        if self.maximized:

            # SECTION Contour
            padding = 10
            text_w, text_h = self.checkbox.get_size()

            lines = []
            lines.append((self.rect.x + padding * 2 + text_w, self.rect.y))
            lines.append((self.rect.x + self.rect.width, self.rect.y))
            lines.append((self.rect.x + self.rect.width, self.rect.y + self.rect.height))
            lines.append((self.rect.x , self.rect.y + self.rect.height))
            lines.append((self.rect.x , self.rect.y))
            lines.append((self.rect.x + padding, self.rect.y))
            pygame.draw.lines(screen, self.color, False, lines, 2)

            for i in range(0, len(self.buttons)):
                if self.selected_option == i : self.button_click(i)
                self.buttons[i].draw(screen)

    def handle_event(self, event):
        self.checkbox.handle_event(event)
        for i in range(0, len(self.buttons)):
            self.buttons[i].handle_event(event)


    def button_click(self, idx):
        self.selected_option = int(idx)
        for i in range(0, len(self.buttons)):
            self.buttons[i].set_base_color(GREEN if i == int(idx) else WHITE)

    def get_value(self):
        return self.buttons[self.selected_option].text


def type_word(word, delais: float):
    global last_keystroke, upper

    now = time.time()

    if (now - last_keystroke) > delais:
        last_keystroke = now
        output = ""
        if upper:
            output = word.upper()
        else:
            output = word

        print(output)

        write_to_cursor(output)

        upper = not upper


def type_paste(first_string, second_string, delais: float):
    global a_string, copied_glob, last_keystroke, first_copy
    now = time.time()
    if (now - last_keystroke) > delais:
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
    global dname
    COLOUR_KEY = (150, 150, 150)  # gray

    first_string = "o"
    second_string = "k"
    idx = 0
    delais = 1.5
    
    # File path
    file_path = os.path.join(str(Path.home()), "zppControllerToChatV2Save.json")

    # Step 1: Check if the file exists
    if os.path.exists(file_path):
        # Step 2: Read and parse the JSON file with UTF-8 encoding
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if (
                    "first_string" in data and "second_string" in data and
                    "idx" in data and "R" in data and "G" in data and "B" in data and
                    "delais" in data
                    ):
                    first_string = str(data["first_string"])
                    second_string = str(data["second_string"])
                    idx = int(data["idx"])
                    r = int(data["R"])
                    g = int(data["G"])
                    b = int(data["B"])
                    COLOUR_KEY = (r, g, b)
                    delais = float(data["delais"])
                    print("Données récupérées :)")
            except json.JSONDecodeError:
                print("Error: File content is not valid JSON.")

    idx_tmp = idx
    COLOUR_KEY_tmp = COLOUR_KEY
    delais_tmp = delais

    app = ControllerOverlayApp(first_string, second_string, idx, idx_tmp, COLOUR_KEY, COLOUR_KEY_tmp, file_path, delais, delais_tmp)
    app.run()
    pygame.quit()
            


if __name__ == "__main__":
    main()
