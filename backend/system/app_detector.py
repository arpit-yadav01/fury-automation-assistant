# system/app_detector.py

import pygetwindow as gw


def get_active_window():

    try:
        win = gw.getActiveWindow()

        if not win:
            return None

        return win.title.lower()

    except Exception as e:
        print("Active window error:", e)
        return None