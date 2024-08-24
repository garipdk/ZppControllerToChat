import pygame
from pynput.keyboard import Key, Controller
import time
import pyperclip
import os
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

upper = False
keyboard = Controller()
last_keystroke = time.time() - 2.
first_copy = last_keystroke


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

def type_paste():
	global a_char, copied_glob, last_keystroke, first_copy
	now = time.time()
	if (now - last_keystroke) > 1.5:
		last_keystroke = now
		copied = pyperclip.paste()
		if copied[:len(copied_glob)] == copied_glob:
			if (now - first_copy) > 30:
				first_copy = now
				pyperclip.copy(copied_glob)
				a_char = 'o'
			else:
				pyperclip.copy(copied + " " + a_char)
				if a_char == 'o':
					a_char = 'k'
				else:
					a_char = 'o'
		else:
			first_copy = now
			copied_glob = copied
			pyperclip.copy(copied)
			a_char = 'o'

		print(pyperclip.paste())
		press_combined_key(Key.ctrl, 'a')
		press_combined_key(Key.ctrl, 'v')
		press_key(Key.enter)

def write_to_cursor(word):
	save_copied = pyperclip.paste()
	pyperclip.copy(word)

	press_combined_key(Key.ctrl, 'a')
	press_combined_key(Key.ctrl, 'v')
	press_key(Key.enter)
	time.sleep(0.1)
	pyperclip.copy(save_copied)

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

pygame.init()

print(pygame.joystick.get_count())


screen = pygame.display.set_mode((100,100), pygame.HIDDEN)
   
joysticks = {}

joycon = 0

while True:
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			pygame.quit()
			exit(0)

		if event.type == pygame.JOYDEVICEADDED:
			joy = pygame.joystick.Joystick(event.device_index)
			joysticks[joy.get_instance_id()] = joy
			print(f"Joystick {joy.get_instance_id()} connencted")

		if event.type == pygame.JOYDEVICEREMOVED and event.instance_id in joysticks:

			del joysticks[event.instance_id]
			print(f"Joystick {event.instance_id} disconnected")

	for joystick in joysticks.values():
		if (joystick.get_button(0) == 1):
			type_word("a")

		if (joystick.get_button(1) == 1):
			type_word("b")

		if (joystick.get_button(2) == 1):
			type_word("x")

		if (joystick.get_button(3) == 1):
			type_word("y")

		if (joystick.get_button(11) == 1):
		    type_word("haut")

		if (joystick.get_button(12) == 1):
			type_word("bas")

		if (joystick.get_button(13) == 1):
			type_word("droite")

		if (joystick.get_button(14) == 1):
			type_word("gauche")

		if joystick.get_button(7) == 1 if "xbox" in joystick.get_name().lower() else joystick.get_button(6) == 1:
			type_word("start")

		if joystick.get_numhats() > 0:
			hat = joystick.get_hat(0)

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
