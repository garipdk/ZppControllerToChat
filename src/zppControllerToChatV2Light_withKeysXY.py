import pygame
from pynput.keyboard import Key, Controller
import time
import os
import platform
is_linux = False
if platform.system() == "Linux":
    is_linux = True
else:
    import pyperclip

from time import sleep
import sys
import json
from pathlib import Path

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

upper = False
keyboard = Controller()
a_string = ""
copied_glob = ""
import tkinter as tk

def get_clipboard_data():
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        clipboard_data = root.clipboard_get()
        
        # Check if the clipboard data is a string
        if isinstance(clipboard_data, str):
            return clipboard_data
        else:
            return ""
    except tk.TclError:
        return ""  # Return an empty string in case of an error

def set_clipboard_data(data):
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # Check if the provided data is a string, if not use an empty string
        if not isinstance(data, str):
            data = ""
        
        root.clipboard_clear()  # Clear the current clipboard contents
        root.clipboard_append(data)  # Append new content to the clipboard
        root.update()  # Required to update clipboard content
    except tk.TclError:
        pass


if is_linux:
    copied_glob = get_clipboard_data()
else:
    copied_glob = pyperclip.paste()
last_keystroke = time.time() - 2.0
first_copy = last_keystroke

class ControllerOverlayApp:

    def __init__(
        self, first_string, second_string, delais,
        trigger_deadzone: float = 0.002,
    ):
        self.first_string, self.second_string, self.delais = first_string, second_string, delais
        

        self.running = False
        self.window_size = (10, 10)
        
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
        # Create an initial window (this will be resized)
        pygame.display.set_mode(self.window_size, pygame.HIDDEN)
        pygame.display.set_caption("Manette Zpp")

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

                if joystick.get_button(1) == 1:
                    type_word("b", self.delais)

                if joystick.get_button(2) == 1:
                    type_word("x", self.delais)

                if joystick.get_button(3) == 1:
                    type_word("y", self.delais)

                if current_controller_type == "xbox1":
                    num_tmp = joystick.get_button(5)
                else:
                    num_tmp = joystick.get_button(10)

                if num_tmp == 1:
                    type_paste(self.first_string, self.second_string, self.delais)

                if joystick.get_button(11) == 1:
                    type_word("haut", self.delais)

                if joystick.get_button(12) == 1:
                    type_word("bas", self.delais)

                if joystick.get_button(13) == 1:
                    type_word("droite", self.delais)

                if joystick.get_button(14) == 1:
                    type_word("gauche", self.delais)

                num_tmp = 0
                if current_controller_type == "xbox1":
                    num_tmp = joystick.get_button(7)
                else:
                    num_tmp = joystick.get_button(6)

                if num_tmp == 1:
                    type_word("start", self.delais)

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

                    if hat[1] == -1:
                        type_word("bas", self.delais)

                    if hat[0] == 1:
                        type_word("droite", self.delais)

                    if hat[0] == -1:
                        type_word("gauche", self.delais)

                axes = joystick.get_numaxes()

                if axes >= 2:
                    x = joystick.get_axis(0)
                    y = joystick.get_axis(1)
                    if y >= 0.5 and x < 0.5 and x > -0.5:
                        type_word("bas", self.delais)
                    elif y <= -0.5 and x < 0.5 and x > -0.5:
                        type_word("haut", self.delais)
                    elif x <= -0.5 and y < 0.5 and y > -0.5:
                        type_word("gauche", self.delais)
                    elif x >= 0.5 and y < 0.5 and y > -0.5:
                        type_word("droite", self.delais)

                if axes >= 4:
                    x = joystick.get_axis(2)
                    y = joystick.get_axis(3)
                    if y >= 0.5 and x < 0.5 and x > -0.5:
                        type_word("bas", self.delais)
                    elif y <= -0.5 and x < 0.5 and x > -0.5:
                        type_word("haut", self.delais)
                    elif x <= -0.5 and y < 0.5 and y > -0.5:
                        type_word("gauche", self.delais)
                    elif x >= 0.5 and y < 0.5 and y > -0.5:
                        type_word("droite", self.delais)


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
        copied = ""
        if is_linux:
            copied = get_clipboard_data()
        else:
            copied = pyperclip.paste()
        if copied[: len(copied_glob)] == copied_glob:
            if (now - first_copy) > 30:
                first_copy = now
                if is_linux:
                    set_clipboard_data(copied_glob)
                else:
                    pyperclip.copy(copied_glob)

                a_string = first_string
            else:
                if is_linux:
                    set_clipboard_data(copied + " " + a_string)
                else:
                    pyperclip.copy(copied + " " + a_string)

                if a_string == first_string:
                    a_string = second_string
                else:
                    a_string = first_string
        else:
            first_copy = now
            copied_glob = copied
            if is_linux:
                set_clipboard_data(copied_glob)
            else:
                pyperclip.copy(copied_glob)

            a_string = first_string

        if is_linux:
            print(get_clipboard_data())
        else:
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
    first_string = "o"
    second_string = "k"
    delais = 1.5
    
    # File path
    file_path = os.path.join(str(Path.home()), "zppControllerToChatV2Save.json")

    # Step 1: Check if the file exists
    print(f"fichier de sauvegarde : \"{file_path}\"")
    if os.path.exists(file_path):
        # Step 2: Read and parse the JSON file with UTF-8 encoding
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if (
                    "first_string" in data and "second_string" in data and "delais" in data
                    ):
                    first_string = str(data["first_string"])
                    second_string = str(data["second_string"])
                    if first_string != second_string:
                        print(f"Données des phrases de spam récupérées du fichier de sauvegarde :)")
                    else:
                        print(f"Données des phrases de spam non récupérées du fichier de sauvegarde :(")
                        print("Les deux phrases sont identiques ...")
                        first_string = "o"
                        second_string = "k"
                    delais = float(data["delais"])
                    
            except json.JSONDecodeError:
                print("Error: File content is not valid JSON.")
    else:
        data = {
                "first_string": first_string,
                "second_string": second_string,
                "idx": 0,
                "R": 150,
                "G": 150,
                "B": 150,
                "delais" : delais,
            }

        with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                print("Données sauvegardées :)")

    print("(modifier les valeur du ficier de sauvegarde à la main pour les charger au relancement du logiciel)")

    app = ControllerOverlayApp(first_string, second_string, delais)
    app.run()
    pygame.quit()
            


if __name__ == "__main__":
    main()
