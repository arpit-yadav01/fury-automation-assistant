# # brain/tab_intelligence.py
# # STEP 134 — Tab intelligence
# # FIX: always opens web versions in browser, not desktop apps

# import time
# import pygetwindow as gw

# try:
#     import win32gui
#     import win32con
#     HAS_WIN32 = True
# except ImportError:
#     HAS_WIN32 = False

# # -------------------------
# # PLATFORM PATTERNS
# # Matches against Chrome window titles
# # -------------------------

# PLATFORM_PATTERNS = {
#     "leetcode":    ["leetcode.com", "leetcode"],
#     "linkedin":    ["linkedin.com", "linkedin"],
#     "naukri":      ["naukri.com", "naukri"],
#     "indeed":      ["indeed.com", "indeed"],
#     "internshala": ["internshala.com", "internshala"],
#     "monster":     ["monster.com", "monster"],
#     "unstop":      ["unstop.com", "unstop"],
#     "wellfound":   ["wellfound.com", "wellfound"],
#     "gmail":       ["gmail.com", "gmail", "mail.google"],
#     "github":      ["github.com", "github"],
#     "youtube":     ["youtube.com", "youtube"],
#     "google":      ["google.com", "google"],
#     "whatsapp":    ["web.whatsapp.com", "whatsapp web", "whatsapp"],
#     "telegram":    ["web.telegram.org", "telegram web", "telegram"],
#     "twitter":     ["twitter.com", "x.com"],
#     "stackoverflow": ["stackoverflow.com"],
#     "codechef":    ["codechef.com"],
#     "codeforces":  ["codeforces.com"],
#     "hackerrank":  ["hackerrank.com"],
# }

# # -------------------------
# # WEB URLs — always use browser
# # Never open desktop apps for these
# # -------------------------

# WEB_URLS = {
#     "leetcode":    "https://leetcode.com",
#     "naukri":      "https://www.naukri.com",
#     "indeed":      "https://www.indeed.com",
#     "internshala": "https://internshala.com",
#     "linkedin":    "https://www.linkedin.com",
#     "gmail":       "https://mail.google.com",
#     "github":      "https://github.com",
#     "whatsapp":    "https://web.whatsapp.com",    # ← web version
#     "telegram":    "https://web.telegram.org",    # ← web version
#     "youtube":     "https://www.youtube.com",
#     "google":      "https://www.google.com",
#     "twitter":     "https://twitter.com",
#     "unstop":      "https://unstop.com",
#     "wellfound":   "https://wellfound.com",
#     "monster":     "https://www.monster.com",
# }


# # -------------------------
# # FIND TAB
# # -------------------------

# def find_tab(platform):
#     """Find an open Chrome/Brave tab for a platform."""
#     patterns = PLATFORM_PATTERNS.get(platform.lower(), [platform.lower()])
#     all_windows = gw.getAllWindows()

#     for w in all_windows:
#         if not w.title:
#             continue
#         title = w.title.lower()
#         # must be a browser window
#         if not any(b in title for b in ["chrome", "chromium", "brave", "firefox", "edge"]):
#             continue
#         for pattern in patterns:
#             if pattern in title:
#                 return {"title": w.title, "hwnd": w._hWnd, "platform": platform}
#     return None


# def find_any_tab(platforms):
#     for platform in platforms:
#         tab = find_tab(platform)
#         if tab:
#             return platform, tab
#     return None, None


# # -------------------------
# # SWITCH TO TAB
# # -------------------------

# def switch_to_tab(platform):
#     """Switch to existing tab or open fresh in browser."""
#     tab = find_tab(platform)
#     if tab:
#         print(f"Found {platform} tab: {tab['title']}")
#         if _focus_window(tab["hwnd"]):
#             print(f"Switched to {platform}")
#             return True
#     print(f"No {platform} tab — opening in browser")
#     return _open_in_browser(platform)


# def _focus_window(hwnd):
#     if not HAS_WIN32:
#         return False
#     try:
#         if win32gui.IsIconic(hwnd):
#             win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
#             time.sleep(0.3)
#         win32gui.SetForegroundWindow(hwnd)
#         time.sleep(0.3)
#         return True
#     except Exception as e:
#         print(f"Focus error: {e}")
#         return False


# def _open_in_browser(platform):
#     """Open platform URL in browser — NEVER opens desktop app."""
#     url = WEB_URLS.get(platform.lower())
#     if not url:
#         url = f"https://www.{platform}.com"

#     print(f"Opening {platform} in browser: {url}")
#     try:
#         from browser.browser_agent import open_website
#         open_website(url)
#         time.sleep(3)
#         return True
#     except Exception as e:
#         print(f"Browser open error: {e}")
#         # fallback to webbrowser module
#         import webbrowser
#         webbrowser.open(url)
#         time.sleep(3)
#         return True


# # -------------------------
# # NAVIGATE TO PLATFORM
# # Main entry point for all Phase 10 agents
# # -------------------------

# def navigate_to_platform(platform):
#     """
#     Find existing tab or open platform in browser.
#     Always uses web version — never desktop apps.
#     """
#     print(f"\n🔍 Navigating to {platform}...")
#     open_tabs = scan_open_tabs()

#     if platform.lower() in open_tabs:
#         print(f"✅ Found {platform} tab — switching")
#         return switch_to_tab(platform)
#     else:
#         print(f"📂 {platform} not open — launching in browser")
#         return _open_in_browser(platform)


# # -------------------------
# # SCAN ALL TABS
# # -------------------------

# def scan_open_tabs():
#     """Scan all open browser tabs and return known platforms."""
#     all_windows = gw.getAllWindows()
#     found = {}

#     for w in all_windows:
#         if not w.title:
#             continue
#         title = w.title.lower()
#         if not any(b in title for b in ["chrome", "chromium", "brave", "firefox", "edge"]):
#             continue
#         for platform, patterns in PLATFORM_PATTERNS.items():
#             for pattern in patterns:
#                 if pattern in title:
#                     if platform not in found:
#                         found[platform] = w.title
#                     break
#     return found


# def print_open_tabs():
#     """Print all known platform tabs currently open."""
#     tabs = scan_open_tabs()
#     print("\n--- Open platform tabs ---")
#     if not tabs:
#         print("  No known platforms found in browser tabs")
#         print("  Open some websites first (Gmail, LeetCode, etc.)")
#     else:
#         for platform, title in tabs.items():
#             print(f"  ✅ {platform:<15} — {title[:50]}")
#     print("--------------------------\n")
#     return tabs



# brain/tab_intelligence.py
# STEP 134 — Tab intelligence
# FIX: opens each platform in a NEW tab
# FIX: uses real Chrome, not Chrome for Testing

import os
import time
import subprocess
import pygetwindow as gw

try:
    import win32gui
    import win32con
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

# -------------------------
# BROWSER DETECTION
# Finds real Chrome or Brave — NOT Chrome for Testing
# -------------------------

BROWSER_PATHS = [
    # Real Chrome
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
    # Brave (great alternative)
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
    # Edge
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    # Chrome for Testing (fallback only)
    os.path.expanduser(r"~\AppData\Local\Google\Chrome for Testing\chrome.exe"),
]

def _get_browser_path():
    """Find the best available browser."""
    for path in BROWSER_PATHS:
        if os.path.exists(path):
            return path
    return None

# -------------------------
# PLATFORM PATTERNS
# -------------------------

PLATFORM_PATTERNS = {
    "leetcode":    ["leetcode.com", "leetcode"],
    "linkedin":    ["linkedin.com", "linkedin"],
    "naukri":      ["naukri.com", "naukri"],
    "indeed":      ["indeed.com", "indeed"],
    "internshala": ["internshala.com", "internshala"],
    "monster":     ["monster.com"],
    "unstop":      ["unstop.com"],
    "wellfound":   ["wellfound.com"],
    "gmail":       ["gmail.com", "mail.google"],
    "github":      ["github.com"],
    "youtube":     ["youtube.com", "youtube"],
    "google":      ["google.com"],
    "whatsapp":    ["web.whatsapp.com", "whatsapp"],
    "telegram":    ["web.telegram.org", "telegram"],
    "twitter":     ["twitter.com", "x.com"],
    "stackoverflow": ["stackoverflow.com"],
    "hackerrank":  ["hackerrank.com"],
}

WEB_URLS = {
    "leetcode":    "https://leetcode.com",
    "naukri":      "https://www.naukri.com",
    "indeed":      "https://www.indeed.com",
    "internshala": "https://internshala.com",
    "linkedin":    "https://www.linkedin.com",
    "gmail":       "https://mail.google.com",
    "github":      "https://github.com",
    "whatsapp":    "https://web.whatsapp.com",
    "telegram":    "https://web.telegram.org",
    "youtube":     "https://www.youtube.com",
    "google":      "https://www.google.com",
}


# -------------------------
# OPEN URL IN NEW TAB
# Always opens in a new tab, never reuses existing tab
# -------------------------

def open_new_tab(url):
    """
    Open a URL in a new browser tab.
    Uses real Chrome/Brave, not Chrome for Testing.
    """
    browser_path = _get_browser_path()

    if browser_path:
        try:
            # --new-tab flag opens in new tab if browser is already running
            subprocess.Popen([browser_path, "--new-tab", url])
            print(f"Opened new tab: {url}")
            time.sleep(3)
            return True
        except Exception as e:
            print(f"Browser open error: {e}")

    # fallback: webbrowser module
    import webbrowser
    webbrowser.open_new_tab(url)
    time.sleep(3)
    return True


# -------------------------
# FIND EXISTING TAB
# -------------------------

def find_tab(platform):
    """Find an open browser tab for a platform."""
    patterns = PLATFORM_PATTERNS.get(platform.lower(), [platform.lower()])
    for w in gw.getAllWindows():
        if not w.title:
            continue
        title = w.title.lower()
        if not any(b in title for b in ["chrome", "brave", "firefox", "edge"]):
            continue
        for pattern in patterns:
            if pattern in title:
                return {"title": w.title, "hwnd": w._hWnd, "platform": platform}
    return None


def _focus_window(hwnd):
    if not HAS_WIN32:
        return False
    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(0.3)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.3)
        return True
    except:
        return False


# -------------------------
# NAVIGATE TO PLATFORM
# Main entry — finds tab or opens new one
# -------------------------

def navigate_to_platform(platform, force_new_tab=False):
    """
    Navigate to a platform.
    - If tab exists and force_new_tab=False: switch to it
    - Otherwise: open in a new tab

    Args:
        platform: platform name e.g. "youtube", "leetcode"
        force_new_tab: always open new tab even if one exists
    """
    print(f"\n🔍 Navigating to {platform}...")

    url = WEB_URLS.get(platform.lower(), f"https://www.{platform}.com")

    if not force_new_tab:
        tab = find_tab(platform)
        if tab:
            print(f"✅ Found {platform} tab — switching")
            if _focus_window(tab["hwnd"]):
                print(f"Switched to {platform}")
                return True

    print(f"📂 Opening {platform} in new tab: {url}")
    return open_new_tab(url)


def switch_to_tab(platform):
    """Switch to existing tab or open new one."""
    return navigate_to_platform(platform)


# -------------------------
# SCAN ALL TABS
# -------------------------

def scan_open_tabs():
    """Scan all open browser tabs and return known platforms."""
    found = {}
    for w in gw.getAllWindows():
        if not w.title:
            continue
        title = w.title.lower()
        if not any(b in title for b in ["chrome", "brave", "firefox", "edge"]):
            continue
        for platform, patterns in PLATFORM_PATTERNS.items():
            for pattern in patterns:
                if pattern in title:
                    if platform not in found:
                        found[platform] = w.title
                    break
    return found


def print_open_tabs():
    """Print all known platforms currently open in browser."""
    tabs = scan_open_tabs()
    browser = _get_browser_path()
    print(f"\n--- Browser: {os.path.basename(browser) if browser else 'unknown'} ---")
    print("--- Open platform tabs ---")
    if not tabs:
        print("  No known platforms open")
        print("  Open Gmail, LeetCode, WhatsApp etc. first")
    else:
        for platform, title in tabs.items():
            print(f"  ✅ {platform:<15} — {title[:50]}")
    print("--------------------------\n")
    return tabs