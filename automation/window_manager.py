# automation/window_manager.py

import time
import pygetwindow as gw


def focus_window(window_name, timeout=5):

    print(f"Searching for window: {window_name}")

    start_time = time.time()

    while time.time() - start_time < timeout:

        windows = gw.getWindowsWithTitle(window_name)

        if windows:
            window = windows[0]
            window.activate()
            print(f"Focused window: {window_name}")
            return True

        time.sleep(0.5)

    print("Window not found.")
    return False