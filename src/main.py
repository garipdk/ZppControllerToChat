import XInput
from pynput.keyboard import Key, Controller
import time
import pyperclip
from randomwordfr import RandomWordFr

a_char = 'O'


class MyHandler(XInput.EventHandler):
    def __init__(self, *controllers, filter=...):
        super().__init__(*controllers, filter=filter)
        self.upper = False
        self.stop = False
        self.copied = pyperclip.paste()
        self.keyboard = Controller()
        self.last_keystroke = time.time() - 2.
        self.first_copy = self.last_keystroke -29

    def process_button_event(self, event):
        if event.type == XInput.EVENT_BUTTON_PRESSED:
            match event.button_id:
                case XInput.BUTTON_DPAD_UP:
                    self.type_word("haut")
                case XInput.BUTTON_DPAD_DOWN:
                    self.type_word("bas")
                case XInput.BUTTON_DPAD_LEFT:
                    self.type_word("gauche")
                case XInput.BUTTON_DPAD_RIGHT:
                    self.type_word("droite")
                case XInput.BUTTON_A:
                    self.type_word("a")
                case XInput.BUTTON_B:
                    self.type_word("b")
                case XInput.BUTTON_START:
                    self.type_word("start")
                case XInput.BUTTON_RIGHT_SHOULDER:
                    self.type_paste()
                case XInput.BUTTON_LEFT_THUMB:
                    self.stop = True
                case _:
                    print(event)


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
        global a_char
        now = time.time()
        if (now - self.last_keystroke) > 1.5:
            self.last_keystroke = now
            copied = pyperclip.paste()
            if copied[:len(self.copied)] == self.copied:
                if (now - self.first_copy) > 30:
                    self.first_copy = now
                    pyperclip.copy(self.copied)
                    a_char = 'O'
                else:
                    pyperclip.copy(copied + " " + a_char)
                    if a_char == 'O':
                        a_char = 'K'
                    else:
                        a_char = 'O'
            else:
                self.first_copy = now
                self.copied = copied
                pyperclip.copy(copied)
                a_char = 'O'

            print(pyperclip.paste())
            self.press_combined_key(Key.ctrl, 'a')
            self.press_combined_key(Key.ctrl, 'v')
            self.press_key(Key.enter)

    def write_to_cursor(self, word):
        save_copied = pyperclip.paste()
        pyperclip.copy(word)

        self.press_combined_key(Key.ctrl, 'a')
        self.press_combined_key(Key.ctrl, 'v')
        self.press_key(Key.enter)

        pyperclip.copy(save_copied)

    def press_key(self, character):
        self.keyboard.press(character)
        self.keyboard.release(character)
    
    def press_combined_key(self, character1, character2):
        self.keyboard.press(character1)
        self.keyboard.press(character2)
        self.keyboard.release(character2)
        self.keyboard.release(character1)


print("ZppControllerToChat")

if not XInput.get_connected()[0]:
    print("Manette non détectée :-(")
    time.sleep(2)
    quit()

filter = XInput.BUTTON_RIGHT_SHOULDER + XInput.STICK_LEFT + XInput.STICK_RIGHT + XInput.BUTTON_DPAD_UP + XInput.BUTTON_DPAD_DOWN + XInput.BUTTON_DPAD_RIGHT + XInput.BUTTON_DPAD_LEFT + XInput.BUTTON_A + XInput.BUTTON_B + XInput.BUTTON_START + XInput.BUTTON_LEFT_THUMB
my_handler = MyHandler(0)
my_handler.set_filter(filter)

print("Lezgo, pour sortir du programme, appuyez sur votre stick gauche.")

my_gamepad_thread = XInput.GamepadThread(my_handler)

while(not my_handler.stop):
    continue

print("Tchao")
time.sleep(2)