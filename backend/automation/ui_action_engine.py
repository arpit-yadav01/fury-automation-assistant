# automation/ui_action_engine.py

import time
import pyautogui

from vision.screen_capture import capture_screen
from vision.ui_verifier import verify_action
from automation.ui_click_engine import safe_click
from execution.recovery_engine import recover_action

from system.app_detector import get_active_window
from system.window_switcher import focus_window

# 🔥 HARD SWITCH (disable all OCR typing)
DISABLE_OCR_TYPING = True


def perform_ui_action(action):

    if not isinstance(action, dict):
        return False

    attempt = 0

    while attempt <= 2:

        # -----------------------
        # ENSURE CORRECT APP
        # -----------------------

        target_app = action.get("app")

        if target_app:
            current = get_active_window()

            if not current or target_app.lower() not in current.lower():
                focus_window(target_app)

        # -----------------------
        # BEFORE STATE
        # -----------------------

        before = capture_screen()

        act = action.get("action")

        print("UIAction:", action)

        # =======================
        # OPEN URL
        # =======================

        if act == "open_url":

            from browser.browser_agent import open_website

            url = action.get("url")

            if url:
                open_website(url)
                return True

        # =======================
        # WAIT
        # =======================

        elif act == "wait":

            time.sleep(action.get("time", 2))
            return True

        # =======================
        # PRESS KEY
        # =======================

        elif act == "press":

            key = action.get("key")

            if key:
                print("Press:", key)
                pyautogui.press(key)
                return True

        # =======================
        # CLICK TEXT (BLOCKED)
        # =======================

        elif act == "click_text":

            if DISABLE_OCR_TYPING:
                print("🚫 OCR click disabled")
                return False

            from vision.ui_click import click_text

            text = action.get("text")

            if text:
                success = click_text(text)
                if success:
                    return True

        # =======================
        # CLICK (XY / BOX)
        # =======================

        elif act == "click":

            safe_click(
                x=action.get("x"),
                y=action.get("y"),
                box=action.get("box")
            )

        # =======================
        # 🔥 TYPE (FINAL FIX)
        # =======================

        elif act == "type":

            text = action.get("text")

            if text:
                print("🔥 FORCE TYPE:", text)

                # 🔥 DIRECT HARD TYPE (bypass everything)
                pyautogui.write(text, interval=0.03)

            return True  # 🔥 STOP HERE (NO FALLBACK)

        # =======================
        # ENTER
        # =======================

        elif act == "enter":

            print("Press: enter")
            pyautogui.press("enter")
            return True

        else:
            print("Unknown UI action:", action)
            return False

        # -----------------------
        # VERIFY
        # -----------------------

        time.sleep(1)

        after = capture_screen()

        result = verify_action(before, after)

        print("Attempt", attempt, "→", result)

        if result.get("success"):
            return True

        # -----------------------
        # RECOVERY
        # -----------------------

        new_action = recover_action(action, attempt)

        if not new_action:
            break

        action = new_action
        attempt += 1

    print("Action failed after retries")

    return False