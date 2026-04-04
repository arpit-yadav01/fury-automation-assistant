# utils/vision/ui_click.py

import pytesseract

# 🔥 TESSERACT PATH (correct)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import time
import pyautogui

from vision.text_detection import find_text_on_screen


# -------------------------
# BASIC CLICK (FIXED)
# -------------------------

def click_text(text):

    position = find_text_on_screen(text)

    if not position:
        print(f"Text '{text}' not found")
        return False

    # -------------------------
    # HANDLE ALL FORMATS
    # -------------------------

    # case 1: dict {"x","y","w","h"}
    if isinstance(position, dict):

        x = int(position["x"] + position["w"] / 2)
        y = int(position["y"] + position["h"] / 2)

    # case 2: tuple/list (x, y)
    elif isinstance(position, (list, tuple)):

        if len(position) == 2:
            x, y = position

        elif len(position) >= 4:
            x = int(position[0] + position[2] / 2)
            y = int(position[1] + position[3] / 2)

        else:
            print("Invalid position:", position)
            return False

    else:
        print("Unknown position format:", position)
        return False

    print(f"Clicking '{text}' at", (x, y))

    pyautogui.moveTo(x, y, duration=0.4)
    pyautogui.click()

    return True


# -------------------------
# SAFE CLICK (retry)
# -------------------------

def click_text_safe(text, retries=3, delay=1):

    for i in range(retries):

        print(f"Searching '{text}' attempt {i+1}")

        position = find_text_on_screen(text)

        if position:

            if isinstance(position, (list, tuple)):

                if len(position) == 2:
                    x, y = position

                elif len(position) >= 4:
                    x = int(position[0] + position[2] / 2)
                    y = int(position[1] + position[3] / 2)

                else:
                    continue

            else:
                continue

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

    if isinstance(position, (list, tuple)):

        if len(position) == 2:
            x, y = position

        elif len(position) >= 4:
            x = int(position[0] + position[2] / 2)
            y = int(position[1] + position[3] / 2)

        else:
            return False

    else:
        return False

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

    if isinstance(position, (list, tuple)):

        if len(position) == 2:
            x, y = position

        elif len(position) >= 4:
            x = int(position[0] + position[2] / 2)
            y = int(position[1] + position[3] / 2)

        else:
            return False

    else:
        return False

    pyautogui.moveTo(x, y, duration=0.4)
    pyautogui.rightClick()

    return True


# -------------------------
# CLICK WITH WAIT
# -------------------------

def click_text_wait(text, wait_before=1):

    time.sleep(wait_before)

    return click_text(text)