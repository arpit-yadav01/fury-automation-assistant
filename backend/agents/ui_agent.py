# agents/ui_agent.py

from agents.base_agent import BaseAgent

from automation.ui_engine import (
    click,
    press,
    hotkey,
    type_text,
)

from automation.typing_engine import smart_type
from automation.window_manager import focus_window

from vision.ui_click import click_text


class UIAgent(BaseAgent):

    def __init__(self):
        super().__init__("UIAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        action = task.get("action")
        intent = task.get("intent")

        if action in ["type", "press", "hotkey", "click"]:
            return True

        if intent in ["type_text", "click_text"]:
            return True

        return False

    # -------------------------

    def handle(self, task):

        action = task.get("action")
        intent = task.get("intent")

        # -----------------
        # WORKFLOW ACTIONS
        # -----------------

        if action == "type":

            text = task.get("text", "")

            type_text(text)

            return

        if action == "press":

            press(task.get("key"))

            return

        if action == "hotkey":

            hotkey(*task.get("keys", []))

            return

        if action == "click":

            click()

            return

        # -----------------
        # SKILL INTENTS
        # -----------------

        if intent == "type_text":

            text = task.get("text")
            window = task.get("window")

            smart_type(text, window)

            return

        if intent == "click_text":

            text = task.get("text")

            click_text(text)

            return