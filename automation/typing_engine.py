# automation/typing_engine.py

import pyautogui
import time


def type_text(text):

    print("Typing in 3 seconds...")

    time.sleep(3)

    pyautogui.write(text, interval=0.05)