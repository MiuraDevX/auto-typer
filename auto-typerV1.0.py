# -*- coding: utf-8 -*-
import keyboard
import pyautogui
import time
import threading
import random
import pyperclip

# Settings
ERROR_PROB = 0.01             # 1% chance of error (very rare)
MIN_INTERVAL = 0.05           # minimum interval between keystrokes
MAX_INTERVAL = 0.15           # maximum interval between keystrokes
WORD_PAUSE_PROB = 0.2         # chance of pausing between words
WORD_PAUSE_RANGE = (0.25, 0.5)
PUNCT_PAUSES = {
    '.': (0.4, 0.9),
    '?': (0.4, 0.9),
    '!': (0.4, 0.9),
    ',': (0.2, 0.5),
}

# Characters that need clipboard paste to work correctly
SPECIAL_CHARS = "çáàâãéêíóôõúüÇÁÀÂÃÉÊÍÓÔÕÚÜ"

running = False
paused = False
text = ""

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

def type_safe(char):
    """Types a character with human-like behavior and accent support."""
    if char in SPECIAL_CHARS:
        pyperclip.copy(char)
        pyautogui.hotkey("ctrl", "v")
    else:
        if char.isalpha() and random.random() < ERROR_PROB:
            wrong = random.choice("abcdefghijklmnopqrstuvwxyz")
            pyautogui.write(wrong)
            time.sleep(random.uniform(0.05, 0.1))
            pyautogui.press("backspace")
            time.sleep(random.uniform(0.04, 0.1))
        pyautogui.write(char)

    time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))

def typer():
    global running, paused, text
    while running:
        if not paused and text:
            for ch in text:
                if not running:
                    break
                while paused and running:
                    time.sleep(0.1)

                type_safe(ch)

                if ch == " " and random.random() < WORD_PAUSE_PROB:
                    time.sleep(random.uniform(*WORD_PAUSE_RANGE))
                if ch in PUNCT_PAUSES:
                    time.sleep(random.uniform(*PUNCT_PAUSES[ch]))

            running = False
        time.sleep(0.08)

def start():
    global running, paused, text
    if not running:
        text = pyperclip.paste()
        running = True
        paused = False
        threading.Thread(target=typer, daemon=True).start()
        print("Started! Text from clipboard will be typed.")

def pause():
    global paused
    paused = not paused
    print("Paused!" if paused else "Resumed!")

def stop():
    global running
    running = False
    print("Stopped!")

# Hotkeys
keyboard.add_hotkey("F8", start)
keyboard.add_hotkey("F9", pause)
keyboard.add_hotkey("F10", stop)

print("F8 = start | F9 = pause/resume | F10 = stop | ESC = exit")
keyboard.wait("esc")
