# automation/window_manager.py

import time
import pygetwindow as gw


# ---------------------------
# EXISTING FUNCTION (KEEP)
# ---------------------------

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


# ---------------------------
# NEW — GET ACTIVE WINDOW
# ---------------------------

def get_active_window():

    try:
        win = gw.getActiveWindow()

        if win:
            return {
                "title": win.title,
                "left": win.left,
                "top": win.top,
                "width": win.width,
                "height": win.height,
            }

    except:
        pass

    return None


# ---------------------------
# NEW — GET ACTIVE WINDOW TITLE
# ---------------------------

def get_active_window_title():

    w = get_active_window()

    if w:
        return w["title"]

    return None


# ---------------------------
# NEW — LIST WINDOWS
# ---------------------------

def list_windows():

    titles = []

    for w in gw.getAllWindows():
        if w.title:
            titles.append(w.title)

    return titles