# agents/multi_app_agent.py

from agents.base_agent import BaseAgent
from system.app_detector import get_active_window
from system.window_switcher import focus_window


class MultiAppAgent(BaseAgent):

    def __init__(self):
        super().__init__("MultiAppAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "ensure_app"

    def handle(self, task):

        target = task.get("app")

        if not target:
            return False

        current = get_active_window()

        print("Current window:", current)
        print("Target app:", target)

        if current and target.lower() in current:
            print("Already focused")
            return True

        return focus_window(target)