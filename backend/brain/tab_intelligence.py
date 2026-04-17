# # brain/tab_intelligence.py
# # STEP 134 — Tab intelligence
# #
# # Finds which of your open Chrome tabs contains a specific platform.
# # Switches to it using keyboard shortcuts.
# # Falls back to opening a fresh tab if not found.
# #
# # Works by reading all window titles visible to pygetwindow.
# # Chrome shows tab titles in the window title bar.

# import time
# import pygetwindow as gw

# try:
#     import win32gui
#     import win32con
#     HAS_WIN32 = True
# except ImportError:
#     HAS_WIN32 = False

# # -------------------------
# # PLATFORM URL MAP
# # Maps platform names to URL fragments to match in tab titles
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
#     "whatsapp":    ["web.whatsapp.com", "whatsapp"],
#     "telegram":    ["web.telegram.org", "telegram"],
#     "twitter":     ["twitter.com", "x.com"],
#     "stackoverflow": ["stackoverflow.com"],
#     "codechef":    ["codechef.com"],
#     "codeforces":  ["codeforces.com"],
#     "hackerrank":  ["hackerrank.com"],
# }


# # -------------------------
# # FIND TAB
# # -------------------------

# def find_tab(platform):
#     """
#     Find an open Chrome tab for a platform.

#     Args:
#         platform: platform name e.g. "leetcode", "naukri", "gmail"

#     Returns:
#         dict with title and hwnd if found, else None
#     """
#     patterns = PLATFORM_PATTERNS.get(platform.lower(), [platform.lower()])

#     all_windows = gw.getAllWindows()

#     for w in all_windows:
#         if not w.title:
#             continue
#         title = w.title.lower()

#         # must be a Chrome window
#         if "chrome" not in title and "chromium" not in title:
#             continue

#         for pattern in patterns:
#             if pattern in title:
#                 return {
#                     "title": w.title,
#                     "hwnd": w._hWnd,
#                     "platform": platform
#                 }

#     return None


# def find_any_tab(platforms):
#     """
#     Find the first available tab from a list of platforms.
#     Returns (platform, tab_info) or (None, None).
#     """
#     for platform in platforms:
#         tab = find_tab(platform)
#         if tab:
#             return platform, tab
#     return None, None


# # -------------------------
# # SWITCH TO TAB
# # -------------------------

# def switch_to_tab(platform):
#     """
#     Switch Chrome focus to the tab containing platform.
#     Opens a fresh tab if not found.

#     Returns True if switched/opened successfully.
#     """
#     tab = find_tab(platform)

#     if tab:
#         print(f"Found {platform} tab: {tab['title']}")
#         success = _focus_chrome_window(tab["hwnd"])
#         if success:
#             print(f"Switched to {platform} tab")
#             return True

#     # not found — open fresh
#     print(f"No {platform} tab found — opening fresh")
#     return _open_platform(platform)


# def _focus_chrome_window(hwnd):
#     """Force a Chrome window to the foreground."""
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
#         print(f"Tab focus error: {e}")
#         return False


# def _open_platform(platform):
#     """Open a platform URL in a new browser tab."""
#     from brain.personal_profile import profile
#     from browser.browser_agent import open_website

#     url = profile.get_platform_url(platform)
#     if not url:
#         # fallback URLs for common platforms
#         fallback = {
#             "leetcode":    "https://leetcode.com",
#             "naukri":      "https://www.naukri.com",
#             "indeed":      "https://www.indeed.com",
#             "internshala": "https://internshala.com",
#             "linkedin":    "https://www.linkedin.com",
#             "gmail":       "https://mail.google.com",
#             "github":      "https://github.com",
#             "whatsapp":    "https://web.whatsapp.com",
#             "telegram":    "https://web.telegram.org",
#         }
#         url = fallback.get(platform.lower(), f"https://www.{platform}.com")

#     print(f"Opening {platform}: {url}")
#     open_website(url)
#     time.sleep(3)
#     return True


# # -------------------------
# # SCAN ALL TABS
# # -------------------------

# def scan_open_tabs():
#     """
#     Scan all open Chrome tabs and return which platforms are open.
#     Useful for showing Fury what accounts are currently active.
#     """
#     all_windows = gw.getAllWindows()
#     found = {}

#     for w in all_windows:
#         if not w.title:
#             continue
#         title = w.title.lower()
#         if "chrome" not in title and "chromium" not in title:
#             continue

#         for platform, patterns in PLATFORM_PATTERNS.items():
#             for pattern in patterns:
#                 if pattern in title:
#                     if platform not in found:
#                         found[platform] = w.title
#                     break

#     return found


# def print_open_tabs():
#     """Print which platforms are currently open in Chrome."""
#     tabs = scan_open_tabs()
#     print("\n--- Open platform tabs ---")
#     if not tabs:
#         print("  No known platforms found in Chrome tabs")
#     else:
#         for platform, title in tabs.items():
#             print(f"  ✅ {platform:<15} — {title[:50]}")
#     print("--------------------------\n")
#     return tabs


# # -------------------------
# # SMART NAVIGATE
# # Used by visual agent — find tab or open platform
# # -------------------------

# def navigate_to_platform(platform):
#     """
#     Smart navigation: find existing tab or open fresh.
#     This is what all Phase 10 agents call first.

#     Returns True if successfully on the platform.
#     """
#     print(f"\n🔍 Looking for {platform}...")

#     # first scan what's open
#     open_tabs = scan_open_tabs()

#     if platform.lower() in open_tabs:
#         print(f"✅ Found {platform} in open tabs")
#         return switch_to_tab(platform)
#     else:
#         print(f"📂 {platform} not open — launching")
#         return _open_platform(platform)




# brain/tab_intelligence.py
# STEP 134 — Tab intelligence
# FIX: always opens web versions in browser, not desktop apps

import time
import pygetwindow as gw

try:
    import win32gui
    import win32con
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

# -------------------------
# PLATFORM PATTERNS
# Matches against Chrome window titles
# -------------------------

PLATFORM_PATTERNS = {
    "leetcode":    ["leetcode.com", "leetcode"],
    "linkedin":    ["linkedin.com", "linkedin"],
    "naukri":      ["naukri.com", "naukri"],
    "indeed":      ["indeed.com", "indeed"],
    "internshala": ["internshala.com", "internshala"],
    "monster":     ["monster.com", "monster"],
    "unstop":      ["unstop.com", "unstop"],
    "wellfound":   ["wellfound.com", "wellfound"],
    "gmail":       ["gmail.com", "gmail", "mail.google"],
    "github":      ["github.com", "github"],
    "youtube":     ["youtube.com", "youtube"],
    "google":      ["google.com", "google"],
    "whatsapp":    ["web.whatsapp.com", "whatsapp web", "whatsapp"],
    "telegram":    ["web.telegram.org", "telegram web", "telegram"],
    "twitter":     ["twitter.com", "x.com"],
    "stackoverflow": ["stackoverflow.com"],
    "codechef":    ["codechef.com"],
    "codeforces":  ["codeforces.com"],
    "hackerrank":  ["hackerrank.com"],
}

# -------------------------
# WEB URLs — always use browser
# Never open desktop apps for these
# -------------------------

WEB_URLS = {
    "leetcode":    "https://leetcode.com",
    "naukri":      "https://www.naukri.com",
    "indeed":      "https://www.indeed.com",
    "internshala": "https://internshala.com",
    "linkedin":    "https://www.linkedin.com",
    "gmail":       "https://mail.google.com",
    "github":      "https://github.com",
    "whatsapp":    "https://web.whatsapp.com",    # ← web version
    "telegram":    "https://web.telegram.org",    # ← web version
    "youtube":     "https://www.youtube.com",
    "google":      "https://www.google.com",
    "twitter":     "https://twitter.com",
    "unstop":      "https://unstop.com",
    "wellfound":   "https://wellfound.com",
    "monster":     "https://www.monster.com",
}


# -------------------------
# FIND TAB
# -------------------------

def find_tab(platform):
    """Find an open Chrome/Brave tab for a platform."""
    patterns = PLATFORM_PATTERNS.get(platform.lower(), [platform.lower()])
    all_windows = gw.getAllWindows()

    for w in all_windows:
        if not w.title:
            continue
        title = w.title.lower()
        # must be a browser window
        if not any(b in title for b in ["chrome", "chromium", "brave", "firefox", "edge"]):
            continue
        for pattern in patterns:
            if pattern in title:
                return {"title": w.title, "hwnd": w._hWnd, "platform": platform}
    return None


def find_any_tab(platforms):
    for platform in platforms:
        tab = find_tab(platform)
        if tab:
            return platform, tab
    return None, None


# -------------------------
# SWITCH TO TAB
# -------------------------

def switch_to_tab(platform):
    """Switch to existing tab or open fresh in browser."""
    tab = find_tab(platform)
    if tab:
        print(f"Found {platform} tab: {tab['title']}")
        if _focus_window(tab["hwnd"]):
            print(f"Switched to {platform}")
            return True
    print(f"No {platform} tab — opening in browser")
    return _open_in_browser(platform)


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
    except Exception as e:
        print(f"Focus error: {e}")
        return False


def _open_in_browser(platform):
    """Open platform URL in browser — NEVER opens desktop app."""
    url = WEB_URLS.get(platform.lower())
    if not url:
        url = f"https://www.{platform}.com"

    print(f"Opening {platform} in browser: {url}")
    try:
        from browser.browser_agent import open_website
        open_website(url)
        time.sleep(3)
        return True
    except Exception as e:
        print(f"Browser open error: {e}")
        # fallback to webbrowser module
        import webbrowser
        webbrowser.open(url)
        time.sleep(3)
        return True


# -------------------------
# NAVIGATE TO PLATFORM
# Main entry point for all Phase 10 agents
# -------------------------

def navigate_to_platform(platform):
    """
    Find existing tab or open platform in browser.
    Always uses web version — never desktop apps.
    """
    print(f"\n🔍 Navigating to {platform}...")
    open_tabs = scan_open_tabs()

    if platform.lower() in open_tabs:
        print(f"✅ Found {platform} tab — switching")
        return switch_to_tab(platform)
    else:
        print(f"📂 {platform} not open — launching in browser")
        return _open_in_browser(platform)


# -------------------------
# SCAN ALL TABS
# -------------------------

def scan_open_tabs():
    """Scan all open browser tabs and return known platforms."""
    all_windows = gw.getAllWindows()
    found = {}

    for w in all_windows:
        if not w.title:
            continue
        title = w.title.lower()
        if not any(b in title for b in ["chrome", "chromium", "brave", "firefox", "edge"]):
            continue
        for platform, patterns in PLATFORM_PATTERNS.items():
            for pattern in patterns:
                if pattern in title:
                    if platform not in found:
                        found[platform] = w.title
                    break
    return found


def print_open_tabs():
    """Print all known platform tabs currently open."""
    tabs = scan_open_tabs()
    print("\n--- Open platform tabs ---")
    if not tabs:
        print("  No known platforms found in browser tabs")
        print("  Open some websites first (Gmail, LeetCode, etc.)")
    else:
        for platform, title in tabs.items():
            print(f"  ✅ {platform:<15} — {title[:50]}")
    print("--------------------------\n")
    return tabs