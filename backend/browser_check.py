# Run this once: python browser_check.py
# It will show you which browsers are installed

import os
import subprocess

browsers = {
    "Chrome":         r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "Chrome (x86)":   r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "Chrome User":    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
    "Brave":          r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "Brave (x86)":    r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
    "Edge":           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "Firefox":        r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "Chrome Testing": os.path.expanduser(r"~\AppData\Local\Google\Chrome for Testing\chrome.exe"),
}

print("=== Installed Browsers ===")
found = []
for name, path in browsers.items():
    if os.path.exists(path):
        print(f"  ✅ {name}: {path}")
        found.append((name, path))
    else:
        print(f"  ❌ {name}: not found")

print(f"\nFound {len(found)} browser(s)")

# also check what's running right now
print("\n=== Browser windows open right now ===")
import pygetwindow as gw
for w in gw.getAllWindows():
    if any(b in w.title.lower() for b in ["chrome", "brave", "firefox", "edge"]):
        if w.title:
            print(f"  {w.title[:80]}")