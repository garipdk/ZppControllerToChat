import XInput
from XInput import get_state
from pynput.keyboard import Key, Controller
import time
import pyperclip

a_char = ""
copied_glob = pyperclip.paste()


class MyHandler(XInput.EventHandler):

    def __init__(self, *controllers, filter=...):
        super().__init__(*controllers, filter=filter)
        self.upper = False
        self.stop = False
        self.keyboard = Controller()
        self.last_keystroke = time.time() - 2.0
        self.first_copy = self.last_keystroke

    def is_button_press(self, button):
        return bool(button & get_state(0).Gamepad.wButtons)

    def process_button_event(self, event):
        if event.type == XInput.EVENT_BUTTON_PRESSED:
            while self.is_button_press(XInput.BUTTON_DPAD_UP):
                self.type_word("haut")
            while self.is_button_press(XInput.BUTTON_DPAD_DOWN):
                self.type_word("bas")
            while self.is_button_press(XInput.BUTTON_DPAD_LEFT):
                self.type_word("gauche")
            while self.is_button_press(XInput.BUTTON_DPAD_RIGHT):
                self.type_word("droite")
            while self.is_button_press(XInput.BUTTON_A):
                self.type_word("a")
            while self.is_button_press(XInput.BUTTON_B):
                self.type_word("b")
            while self.is_button_press(XInput.BUTTON_START):
                self.type_word("start")
            while self.is_button_press(XInput.BUTTON_RIGHT_SHOULDER):
                self.type_paste()
            while self.is_button_press(XInput.BUTTON_LEFT_THUMB):
                self.stop = True

    def process_trigger_event(self, event):
        return

    def process_stick_event(self, event):
        if event.type == XInput.EVENT_STICK_MOVED:
            if event.y >= 0.5 and event.x < 0.5 and event.x > -0.5:
                self.type_word("haut")
            elif event.y <= -0.5 and event.x < 0.5 and event.x > -0.5:
                self.type_word("bas")
            elif event.x <= -0.5 and event.y < 0.5 and event.y > -0.5:
                self.type_word("gauche")
            elif event.x >= 0.5 and event.y < 0.5 and event.y > -0.5:
                self.type_word("droite")

    def process_connection_event(self, event):
        return

    def type_word(self, word):
        now = time.time()

        if (now - self.last_keystroke) > 1.5:
            self.last_keystroke = now
            output = ""
            if self.upper:
                output = word.upper()
            else:
                output = word

            print(output)

            self.write_to_cursor(output)

            self.upper = not self.upper

    def type_paste(self):
        global a_char, copied_glob
        now = time.time()
        if (now - self.last_keystroke) > 1.5:
            self.last_keystroke = now
            copied = pyperclip.paste()
            if copied[: len(copied_glob)] == copied_glob:
                if (now - self.first_copy) > 30:
                    self.first_copy = now
                    pyperclip.copy(copied_glob)
                    a_char = "o"
                else:
                    pyperclip.copy(copied + " " + a_char)
                    if a_char == "o":
                        a_char = "k"
                    else:
                        a_char = "o"
            else:
                self.first_copy = now
                copied_glob = copied
                pyperclip.copy(copied)
                a_char = "o"

            print(pyperclip.paste())
            self.press_combined_key(Key.ctrl, "a")
            self.press_combined_key(Key.ctrl, "v")
            self.press_key(Key.enter)

    def write_to_cursor(self, word):
        save_copied = pyperclip.paste()
        pyperclip.copy(word)

        self.press_combined_key(Key.ctrl, "a")
        self.press_combined_key(Key.ctrl, "v")
        self.press_key(Key.enter)

        pyperclip.copy(save_copied)

    def press_key(self, character):
        self.keyboard.press(character)
        time.sleep(0.001)
        self.keyboard.release(character)
        time.sleep(0.001)

    def press_combined_key(self, character1, character2):
        self.keyboard.press(character1)
        self.keyboard.press(character2)
        time.sleep(0.001)
        self.keyboard.release(character2)
        self.keyboard.release(character1)
        time.sleep(0.001)


print("ZppControllerToChat")

if not XInput.get_connected()[0]:
    print("Manette non détectée :-(")
    time.sleep(2)
    quit()

filter = (
    XInput.BUTTON_RIGHT_SHOULDER
    + XInput.STICK_LEFT
    + XInput.STICK_RIGHT
    + XInput.BUTTON_DPAD_UP
    + XInput.BUTTON_DPAD_DOWN
    + XInput.BUTTON_DPAD_RIGHT
    + XInput.BUTTON_DPAD_LEFT
    + XInput.BUTTON_A
    + XInput.BUTTON_B
    + XInput.BUTTON_START
    + XInput.BUTTON_LEFT_THUMB
)
my_handler = MyHandler(0)
my_handler.set_filter(filter)

print("Lezgo, pour sortir du programme, appuyez sur votre stick gauche.")

my_gamepad_thread = XInput.GamepadThread(my_handler)

while not my_handler.stop:
    continue

print("Tchao")
time.sleep(2)
