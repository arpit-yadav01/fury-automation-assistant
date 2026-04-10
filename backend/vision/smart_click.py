# vision/smart_click.py

import pyautogui
import time
from vision.ui_understanding import find_input_box, find_button, find_element_near_text
from vision.text_detection import find_text_on_screen


def smart_click(target):
    """
    Smart click — tries multiple strategies:
    1. Click by text (OCR)
    2. Click by element type
    3. Click by coordinates
    """

    # strategy 1 — text match
    pos = find_text_on_screen(target)

    if pos:
        x = pos["x"] + pos["w"] // 2
        y = pos["y"] + pos["h"] // 2
        _smooth_click(x, y)
        print(f"Smart click → text match '{target}' at ({x},{y})")
        return True

    # strategy 2 — element type
    if target in ["input", "search", "textbox", "searchbox"]:

        el = find_input_box()

        if el:
            _smooth_click(el["cx"], el["cy"])
            print(f"Smart click → input box at ({el['cx']},{el['cy']})")
            return True

    if target in ["button", "ok", "submit", "confirm"]:

        el = find_button()

        if el:
            _smooth_click(el["cx"], el["cy"])
            print(f"Smart click → button at ({el['cx']},{el['cy']})")
            return True

    # strategy 3 — near text
    el = find_element_near_text(target)

    if el:
        _smooth_click(el["cx"], el["cy"])
        print(f"Smart click → near text '{target}' at ({el['cx']},{el['cy']})")
        return True

    print(f"Smart click → could not find '{target}'")
    return False


def _smooth_click(x, y, duration=0.3):
    """Move to position smoothly then click."""

    pyautogui.moveTo(x, y, duration=duration)
    time.sleep(0.1)
    pyautogui.click()


def click_at(x, y):
    """Direct coordinate click."""
    _smooth_click(x, y)


def click_center_of(element):
    """Click center of a detected element dict."""

    if not element:
        return False

    _smooth_click(element["cx"], element["cy"])
    return True