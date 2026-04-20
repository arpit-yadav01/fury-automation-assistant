# browser/browser_agent.py
# FIXED: uses real Chrome via subprocess — no Playwright
# This stops the "two browser" problem permanently

import os
import subprocess
import time

# -------------------------
# FIND REAL CHROME
# Order: Chrome > Brave > Edge > Chrome for Testing (last resort)
# -------------------------

_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    os.path.expanduser(r"~\AppData\Local\Google\Chrome for Testing\chrome.exe"),
]

_chrome_path = None

def _get_chrome():
    global _chrome_path
    if _chrome_path:
        return _chrome_path
    for path in _PATHS:
        if os.path.exists(path):
            _chrome_path = path
            return path
    return None


def _focus_real_browser():
    """Bring real Chrome/Brave to foreground — skip Chrome for Testing."""
    try:
        import pygetwindow as gw
        import win32gui, win32con
        for w in gw.getAllWindows():
            if not w.title:
                continue
            t = w.title.lower()
            if "for testing" in t:
                continue
            if any(b in t for b in ["chrome", "brave", "firefox", "edge"]):
                hwnd = w._hWnd
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.2)
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.3)
                return True
    except:
        pass
    return False


# -------------------------
# OPEN WEBSITE
# Opens in real Chrome — new tab if already running
# -------------------------

def open_website(url):
    """Open URL in real Chrome. Opens new tab if Chrome is already running."""
    chrome = _get_chrome()
    if chrome:
        try:
            subprocess.Popen([chrome, "--new-tab", url])
            print(f"Opening: {url}")
            time.sleep(2)
            _focus_real_browser()
            return True
        except Exception as e:
            print(f"Chrome error: {e}")
    # fallback
    import webbrowser
    webbrowser.open(url)
    time.sleep(2)
    return True


# -------------------------
# SEARCH ON PAGE
# Types search query in focused browser using pyautogui
# No Playwright needed
# -------------------------

def search_on_page(query, selector=None):
    """Type search in focused browser via address bar."""
    try:
        import pyautogui
        _focus_real_browser()
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "l")
        time.sleep(0.3)
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        pyautogui.write(url, interval=0.03)
        pyautogui.press("enter")
        print(f"Searching: {query}")
        time.sleep(2)
    except Exception as e:
        print(f"Search failed: {e}")


def smart_search(query):
    """Navigate to search URL directly."""
    open_website(f"https://www.google.com/search?q={query.replace(' ', '+')}")
    print(f"Smart search: {query}")