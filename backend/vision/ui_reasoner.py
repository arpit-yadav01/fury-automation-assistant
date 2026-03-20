# vision/ui_reasoner.py

import time

from vision.text_detection import find_text_on_screen
from vision.screen_capture import capture_screen

from brain.context_memory import memory


# -------------------------
# CHECK TEXT EXISTS
# -------------------------

def text_exists(text):

    pos = find_text_on_screen(text)

    # safe validation
    if pos is None:
        return False

    if pos is False:
        return False

    if pos == []:
        return False

    return True


# -------------------------
# WAIT FOR TEXT
# -------------------------

def wait_for_text(text, timeout=5):

    start = time.time()

    while time.time() - start < timeout:

        if text_exists(text):
            return True

        time.sleep(0.5)

    return False


# -------------------------
# SAFE CLICK
# -------------------------

def click_if_exists(text):

    from vision.ui_click import click_text

    if not text_exists(text):

        print("UI not found:", text)

        return False

    click_text(text)

    memory.set_action("click_" + text)

    return True


# -------------------------
# WAIT + CLICK
# -------------------------

def wait_and_click(text, timeout=5):

    ok = wait_for_text(text, timeout)

    if not ok:

        print("Timeout waiting:", text)

        return False

    return click_if_exists(text)