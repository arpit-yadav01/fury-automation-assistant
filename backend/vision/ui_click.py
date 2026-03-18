# utils/vision/ui_click.py

import time
import pyautogui

from vision.text_detection import find_text_on_screen


# -------------------------
# BASIC CLICK
# -------------------------

def click_text(text):

    position = find_text_on_screen(text)

    if position:

        x, y = position

        print(f"Clicking '{text}' at", position)

        pyautogui.moveTo(x, y, duration=0.4)

        pyautogui.click()

        return True

    else:

        print(f"Text '{text}' not found")

        return False


# -------------------------
# SAFE CLICK (retry)
# -------------------------

def click_text_safe(text, retries=3, delay=1):

    for i in range(retries):

        print(f"Searching '{text}' attempt {i+1}")

        position = find_text_on_screen(text)

        if position:

            x, y = position

            pyautogui.moveTo(x, y, duration=0.4)

            pyautogui.click()

            return True

        time.sleep(delay)

    print("Failed to click:", text)

    return False


# -------------------------
# DOUBLE CLICK
# -------------------------

def double_click_text(text):

    position = find_text_on_screen(text)

    if not position:
        print("Not found:", text)
        return False

    x, y = position

    pyautogui.moveTo(x, y, duration=0.4)

    pyautogui.doubleClick()

    return True


# -------------------------
# RIGHT CLICK
# -------------------------

def right_click_text(text):

    position = find_text_on_screen(text)

    if not position:
        print("Not found:", text)
        return False

    x, y = position

    pyautogui.moveTo(x, y, duration=0.4)

    pyautogui.rightClick()

    return True


# -------------------------
# CLICK WITH WAIT
# -------------------------

def click_text_wait(text, wait_before=1):

    time.sleep(wait_before)

    return click_text(text)