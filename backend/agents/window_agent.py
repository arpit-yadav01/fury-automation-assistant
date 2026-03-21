# agents/window_agent.py

from agents.base_agent import BaseAgent

from automation.window_manager import (
    focus_window,
    get_active_window_title,
    list_windows,
)

from brain.context_memory import memory


class WindowAgent(BaseAgent):

    def __init__(self):
        super().__init__("WindowAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        action = task.get("action")
        intent = task.get("intent")

        if action == "focus_window":
            return True

        if intent in [
            "focus_window",
            "get_window",
            "list_windows",
        ]:
            return True

        return False

    # -------------------------

    def handle(self, task):

        action = task.get("action")
        intent = task.get("intent")

        # workflow action

        if action == "focus_window":

            name = task.get("name")

            focus_window(name)

            memory.set_window(name)

            return

        # intents

        if intent == "focus_window":

            name = task.get("window")

            focus_window(name)

            memory.set_window(name)

            return

        if intent == "get_window":

            title = get_active_window_title()

            print("Active:", title)

            memory.set_window(title)

            return

        if intent == "list_windows":

            wins = list_windows()

            print("Windows:", wins)

            return