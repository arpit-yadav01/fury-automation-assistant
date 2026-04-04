import pyautogui
import time

from automation.window_manager import (
    get_active_window_title,
    focus_window,
)

from brain.context_memory import memory


# -------------------------
# BASIC TYPE
# -------------------------

def type_text(text):

    window = memory.get_window()

    if window:
        print("Typing in window:", window)
        focus_window(window)
        time.sleep(0.5)

    print("Typing:", text)

    pyautogui.write(text, interval=0.03)


# -------------------------
# SMART TYPE
# -------------------------

def smart_type(text, window=None, delay=0.5):

    if window:
        focus_window(window)
        time.sleep(0.5)

    else:
        mem_window = memory.get_window()

        if mem_window:
            focus_window(mem_window)
            time.sleep(0.5)

    active = get_active_window_title()
    print("Active window:", active)

    time.sleep(delay)

    print("Smart typing:", text)

    pyautogui.write(text, interval=0.03)


# -------------------------
# TYPE IN SPECIFIC WINDOW
# -------------------------

def type_in_window(window, text):

    ok = focus_window(window)

    if not ok:
        print("Cannot focus window")
        return False

    time.sleep(0.5)

    pyautogui.write(text, interval=0.03)

    return True


# -------------------------
# PRESS KEY
# -------------------------

def press(key):
    print("Press:", key)
    pyautogui.press(key)


# -------------------------
# HOTKEY
# -------------------------

def hotkey(*keys):
    print("Hotkey:", keys)
    pyautogui.hotkey(*keys)