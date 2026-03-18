# automation/typing_engine.py

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
        time.sleep(1)

    print("Typing in 1 second...")
    time.sleep(1)

    pyautogui.write(text, interval=0.05)


# -------------------------
# SMART TYPE
# -------------------------

def smart_type(text, window=None, delay=1):

    if window:

        print("Focusing window:", window)
        focus_window(window)
        time.sleep(1)

    else:

        mem_window = memory.get_window()

        if mem_window:
            print("Using memory window:", mem_window)
            focus_window(mem_window)
            time.sleep(1)

    active = get_active_window_title()

    print("Active window:", active)

    time.sleep(delay)

    pyautogui.write(text, interval=0.03)


# -------------------------
# TYPE IN WINDOW
# -------------------------

def type_in_window(window, text):

    print("Typing in window:", window)

    ok = focus_window(window)

    if not ok:
        print("Cannot focus window")
        return

    time.sleep(1)

    pyautogui.write(text, interval=0.03)


# -------------------------
# PRESS
# -------------------------

def press(key):

    pyautogui.press(key)


# -------------------------
# HOTKEY
# -------------------------

def hotkey(*keys):

    pyautogui.hotkey(*keys)