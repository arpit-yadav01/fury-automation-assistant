# automation/ui_action_engine.py

import time

from vision.screen_capture import capture_screen
from vision.ui_verifier import verify_action
from automation.ui_click_engine import safe_click
from execution.recovery_engine import recover_action

# ✅ NEW (STEP 96)
from system.app_detector import get_active_window
from system.window_switcher import focus_window


def perform_ui_action(action):

    if not isinstance(action, dict):
        return False

    attempt = 0

    while attempt <= 2:

        # -----------------------
        # STEP 96: ENSURE APP
        # -----------------------

        target_app = action.get("app")

        if target_app:
            current = get_active_window()

            if not current or target_app.lower() not in current:
                focus_window(target_app)

        # -----------------------
        # BEFORE STATE
        # -----------------------

        before = capture_screen()

        act = action.get("action")

        # -----------------------
        # CLICK
        # -----------------------

        if act == "click":

            safe_click(
                x=action.get("x"),
                y=action.get("y"),
                box=action.get("box")
            )

        # -----------------------
        # TYPE
        # -----------------------

        elif act == "type":

            from automation.ui_engine import type_text

            text = action.get("text")

            if text:
                type_text(text)

        # -----------------------
        # ENTER
        # -----------------------

        elif act == "enter":

            from automation.ui_engine import press
            press("enter")

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