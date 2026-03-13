import pyautogui
import time

pyautogui.FAILSAFE = True


# =========================
# MOUSE CONTROL
# =========================

def move(x, y, duration=0.2):
    pyautogui.moveTo(x, y, duration=duration)


def click(x=None, y=None):
    if x is not None and y is not None:
        pyautogui.click(x, y)
    else:
        pyautogui.click()


def double_click():
    pyautogui.doubleClick()


def right_click():
    pyautogui.rightClick()


def scroll(amount):
    pyautogui.scroll(amount)


# =========================
# KEYBOARD CONTROL
# =========================

def press(key):
    pyautogui.press(key)


def hotkey(*keys):
    pyautogui.hotkey(*keys)


def type_text(text, interval=0.02):
    pyautogui.write(text, interval=interval)


# =========================
# WAIT / DELAY
# =========================

def wait(seconds):
    time.sleep(seconds)


# =========================
# SCREEN INFO
# =========================

def get_mouse_position():
    return pyautogui.position()


def get_screen_size():
    return pyautogui.size()