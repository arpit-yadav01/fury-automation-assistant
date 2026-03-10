# vision/ui_click.py

import pyautogui
from vision.text_detection import find_text_on_screen


def click_text(text):

    position = find_text_on_screen(text)

    if position:

        x, y = position

        print(f"Clicking on '{text}' at", position)

        pyautogui.moveTo(x, y, duration=0.5)

        pyautogui.click()

    else:

        print(f"Text '{text}' not found on screen")