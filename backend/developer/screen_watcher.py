# developer/screen_watcher.py
# STEP 145 — Screen watcher
#
# Monitors your screen for specific events and alerts you.
# Uses OCR (free, zero tokens) to read screen text periodically.
# No screenshots sent to LLM — all local.
#
# Usage:
#   watch for "new message" on whatsapp
#   watch for "accepted" on leetcode
#   watch for "interview" in email
#   stop watching
#
# Examples:
#   from developer.screen_watcher import watcher
#   watcher.start("new message")
#   watcher.stop()

import os
import time
import threading
import re
from datetime import datetime


class ScreenWatcher:
    """
    Monitors screen text using OCR and alerts when
    a keyword or phrase appears.
    Runs in background thread — doesn't block Fury.
    Zero tokens — pure OCR.
    """

    def __init__(self):
        self._thread   = None
        self._running  = False
        self._watches  = []   # list of {keyword, callback, triggered}
        self._interval = 5    # check every 5 seconds
        self._last_text = ""

    # ─────────────────────────────
    # START WATCHING
    # ─────────────────────────────

    def start(self, keyword, callback=None, interval=5):
        """
        Start watching screen for a keyword.

        Args:
            keyword: text to watch for e.g. "new message", "accepted"
            callback: function to call when found (optional)
                      defaults to printing an alert
            interval: how often to check in seconds (default 5)
        """
        self._interval = interval

        # add to watch list
        self._watches.append({
            "keyword":   keyword.lower(),
            "callback":  callback or self._default_alert,
            "triggered": False,
            "added_at":  str(datetime.now()),
        })

        print(f"\n👁️  Screen watcher: watching for '{keyword}'")
        print(f"   Checking every {interval} seconds")
        print(f"   Type 'stop watching' to stop\n")

        # start background thread if not running
        if not self._running:
            self._running = True
            self._thread  = threading.Thread(
                target=self._watch_loop,
                daemon=True
            )
            self._thread.start()

    def watch_multiple(self, keywords, interval=5):
        """Watch for multiple keywords at once."""
        for kw in keywords:
            self.start(kw, interval=interval)

    # ─────────────────────────────
    # STOP WATCHING
    # ─────────────────────────────

    def stop(self):
        """Stop all screen watching."""
        self._running = False
        self._watches = []
        print("👁️  Screen watcher stopped")

    def clear(self):
        """Clear all watches but keep running."""
        self._watches = []
        print("👁️  All watches cleared")

    def status(self):
        """Show current watches."""
        if not self._watches:
            print("👁️  No active watches")
            return
        print(f"\n👁️  Active watches ({len(self._watches)}):")
        for w in self._watches:
            status = "✅ triggered" if w["triggered"] else "⏳ waiting"
            print(f"   {status} — '{w['keyword']}'")
        print()

    # ─────────────────────────────
    # WATCH LOOP — background thread
    # ─────────────────────────────

    def _watch_loop(self):
        """Main background loop — reads screen via OCR every N seconds."""
        from vision.screen_capture import capture_screen
        import cv2

        while self._running and self._watches:
            try:
                # capture screen
                img = capture_screen()
                if img is None:
                    time.sleep(self._interval)
                    continue

                # OCR — free, zero tokens
                screen_text = self._ocr(img)

                # skip if screen hasn't changed
                if screen_text == self._last_text:
                    time.sleep(self._interval)
                    continue
                self._last_text = screen_text

                # check each watch
                for watch in self._watches:
                    if watch["triggered"]:
                        continue
                    keyword = watch["keyword"]
                    if keyword in screen_text.lower():
                        watch["triggered"] = True
                        watch["callback"](keyword, screen_text)

                # remove all-triggered watches
                active = [w for w in self._watches if not w["triggered"]]
                if len(active) < len(self._watches):
                    self._watches = active

                time.sleep(self._interval)

            except Exception as e:
                time.sleep(self._interval)

        self._running = False

    # ─────────────────────────────
    # OCR
    # ─────────────────────────────

    def _ocr(self, img):
        """Read screen text using pytesseract — free."""
        try:
            import pytesseract
            import cv2
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            return text.lower()
        except:
            return ""

    # ─────────────────────────────
    # DEFAULT ALERT
    # ─────────────────────────────

    def _default_alert(self, keyword, screen_text):
        """Print alert when keyword found."""
        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"\n{'='*50}")
        print(f"🔔 FURY ALERT — {timestamp}")
        print(f"   Found: '{keyword}'")
        print(f"{'='*50}\n")

        # also try Windows notification
        try:
            self._windows_notify(
                title="Fury Alert",
                message=f"Detected: {keyword}"
            )
        except:
            pass

    def _windows_notify(self, title, message):
        """Show Windows toast notification."""
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message,
                               duration=5, threaded=True)
        except ImportError:
            # win10toast not installed — use PowerShell fallback
            try:
                import subprocess
                script = (
                    f'[Windows.UI.Notifications.ToastNotificationManager, '
                    f'Windows.UI.Notifications, ContentType=WindowsRuntime] | '
                    f'Out-Null; '
                    f'$template = [Windows.UI.Notifications.ToastTemplateType]::'
                    f'ToastText01; '
                    f'$xml = [Windows.UI.Notifications.ToastNotificationManager]::'
                    f'GetTemplateContent($template); '
                    f'$xml.GetElementsByTagName("text")[0].AppendChild('
                    f'$xml.CreateTextNode("{title}: {message}")) | Out-Null; '
                    f'$toast = [Windows.UI.Notifications.ToastNotification]::new($xml); '
                    f'[Windows.UI.Notifications.ToastNotificationManager]::'
                    f'CreateToastNotifier("Fury").Show($toast)'
                )
                subprocess.Popen(
                    ["powershell", "-Command", script],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except:
                pass


# ─────────────────────────────
# PRESET WATCHERS
# Common use cases built-in
# ─────────────────────────────

def watch_whatsapp_message(contact=None):
    """Alert when a new WhatsApp message arrives."""
    keyword = f"message from {contact.lower()}" if contact else "new message"
    watcher.start(keyword, interval=3)


def watch_leetcode_result():
    """Alert when LeetCode run/submit completes."""
    watcher.watch_multiple(
        ["accepted", "wrong answer", "runtime error",
         "time limit", "compile error"],
        interval=2
    )


def watch_email(keyword="interview"):
    """Alert when an email with keyword arrives."""
    watcher.start(keyword, interval=10)


def watch_custom(keyword, interval=5):
    """Watch for any custom keyword."""
    watcher.start(keyword, interval=interval)


# ─────────────────────────────
# NATURAL LANGUAGE ROUTER
# ─────────────────────────────

def handle_watch_command(command):
    """
    Route natural language watch commands.

    Examples:
      watch for new message on whatsapp
      watch for accepted on leetcode
      watch for interview in email
      watch whatsapp messages
      watch leetcode result
      stop watching
      watch status
    """
    cmd = command.lower().strip()

    if cmd in ("stop watching", "stop watch", "unwatch"):
        watcher.stop()
        return

    if cmd in ("watch status", "watching", "what am i watching"):
        watcher.status()
        return

    if "whatsapp" in cmd:
        # extract contact if mentioned
        m = re.search(r"(?:from|message from)\s+(\w+)", cmd)
        contact = m.group(1) if m else None
        watch_whatsapp_message(contact)
        return

    if "leetcode" in cmd:
        watch_leetcode_result()
        print("👁️  Watching for LeetCode result...")
        return

    if "email" in cmd or "gmail" in cmd:
        m = re.search(r"(?:for|keyword)\s+['\"]?([a-zA-Z\s]+)['\"]?", cmd)
        keyword = m.group(1).strip() if m else "interview"
        watch_email(keyword)
        return

    # generic "watch for X"
    m = re.search(r"(?:watch for|watch|alert me when|notify when)\s+['\"]?(.+?)['\"]?$", cmd)
    if m:
        keyword = m.group(1).strip()
        watcher.start(keyword)
        return

    print("Watch commands:")
    print("  watch for <keyword>")
    print("  watch whatsapp messages")
    print("  watch leetcode result")
    print("  watch email for interview")
    print("  stop watching")
    print("  watch status")


# ─────────────────────────────
# GLOBAL INSTANCE
# ─────────────────────────────

watcher = ScreenWatcher()