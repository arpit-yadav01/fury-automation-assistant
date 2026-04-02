# system/window_switcher.py

import pygetwindow as gw


def focus_window(name):

    try:

        windows = gw.getWindowsWithTitle(name)

        if not windows:
            print("No window found:", name)
            return False

        win = windows[0]

        win.activate()

        print("Focused window:", win.title)

        return True

    except Exception as e:
        print("Focus error:", e)
        return False