# # automation/window_manager.py

# import time
# import pygetwindow as gw


# # ---------------------------
# # EXISTING FUNCTION (KEEP)
# # ---------------------------
# def focus_window(window_name, timeout=5):

#     print(f"Searching for window: {window_name}")

#     start_time = time.time()

#     window_name = window_name.lower()

#     while time.time() - start_time < timeout:

#         windows = gw.getAllWindows()

#         for w in windows:

#             title = w.title.lower()

#             # partial match instead of exact match
#             if window_name in title:

#                 try:
#                     w.activate()
#                     print("Focused window:", w.title)
#                     return True
#                 except:
#                     pass

#         time.sleep(0.5)

#     print("Window not found.")
#     return False


# # ---------------------------
# # NEW — GET ACTIVE WINDOW
# # ---------------------------

# def get_active_window():

#     try:
#         win = gw.getActiveWindow()

#         if win:
#             return {
#                 "title": win.title,
#                 "left": win.left,
#                 "top": win.top,
#                 "width": win.width,
#                 "height": win.height,
#             }

#     except:
#         pass

#     return None


# # ---------------------------
# # NEW — GET ACTIVE WINDOW TITLE
# # ---------------------------

# def get_active_window_title():

#     w = get_active_window()

#     if w:
#         return w["title"]

#     return None


# # ---------------------------
# # NEW — LIST WINDOWS
# # ---------------------------

# def list_windows():

#     titles = []

#     for w in gw.getAllWindows():
#         if w.title:
#             titles.append(w.title)

#     return titles


# automation/window_manager.py
# FIX: force_focus_window uses win32gui to actually bring window to front
# pygetwindow's activate() often fails silently on Windows

import time
import pygetwindow as gw

try:
    import win32gui
    import win32con
    import win32process
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False


# ---------------------------
# FORCE FOCUS (NEW)
# Uses win32gui to truly bring window to foreground
# ---------------------------

def force_focus_window(window_name, timeout=5):
    """
    Forcefully bring a window to the foreground using win32gui.
    Much more reliable than pygetwindow's activate() on Windows.
    """
    if not HAS_WIN32:
        return focus_window(window_name, timeout)

    window_name = window_name.lower()
    start = time.time()

    while time.time() - start < timeout:
        windows = gw.getAllWindows()

        for w in windows:
            if not w.title or window_name not in w.title.lower():
                continue
            try:
                hwnd = w._hWnd

                # restore if minimized
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.3)

                # bring to foreground
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.3)

                # verify it worked
                active = win32gui.GetForegroundWindow()
                active_title = win32gui.GetWindowText(active).lower()

                if window_name in active_title:
                    print(f"Focused window: {w.title}")
                    return True
                else:
                    # fallback: use ShowWindow then SetForegroundWindow again
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                    win32gui.BringWindowToTop(hwnd)
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.3)
                    print(f"Force focused: {w.title}")
                    return True

            except Exception as e:
                print(f"Force focus error: {e}")

        time.sleep(0.3)

    print(f"Window not found: {window_name}")
    return False


# ---------------------------
# EXISTING FUNCTION (KEEP)
# Kept for backward compatibility
# ---------------------------

def focus_window(window_name, timeout=5):

    print(f"Searching for window: {window_name}")

    # try force focus first (more reliable)
    if HAS_WIN32:
        return force_focus_window(window_name, timeout)

    # fallback to original pygetwindow method
    start_time = time.time()
    window_name = window_name.lower()

    while time.time() - start_time < timeout:
        windows = gw.getAllWindows()
        for w in windows:
            title = w.title.lower()
            if window_name in title:
                try:
                    w.activate()
                    print("Focused window:", w.title)
                    return True
                except:
                    pass
        time.sleep(0.5)

    print("Window not found.")
    return False


# ---------------------------
# GET ACTIVE WINDOW
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


def get_active_window_title():
    w = get_active_window()
    if w:
        return w["title"]
    return None


# ---------------------------
# LIST WINDOWS
# ---------------------------

def list_windows():
    titles = []
    for w in gw.getAllWindows():
        if w.title:
            titles.append(w.title)
    return titles


# ---------------------------
# VERIFY FOCUS
# ---------------------------

def is_window_focused(window_name):
    """Check if a window with this name is currently in the foreground."""
    try:
        if HAS_WIN32:
            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd).lower()
            return window_name.lower() in title
        else:
            win = gw.getActiveWindow()
            return win and window_name.lower() in win.title.lower()
    except:
        return False