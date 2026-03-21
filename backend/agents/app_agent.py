# agents/app_agent.py

from agents.base_agent import BaseAgent

from automation.window_manager import (
    get_active_window_title,
)

from brain.context_memory import memory


class AppDetectionAgent(BaseAgent):

    def __init__(self):
        super().__init__("AppDetectionAgent")

    # -------------------------

    def can_handle(self, task):

        if isinstance(task, dict) and task.get("detect_app"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        title = get_active_window_title()

        if not title:
            return

        t = title.lower()

        print("AppDetection:", t)

        if "chrome" in t:
            memory.set_app("browser")

        elif "code" in t:
            memory.set_app("vscode")

        elif "notepad" in t:
            memory.set_app("notepad")

        elif "cmd" in t or "powershell" in t:
            memory.set_app("terminal")

        else:
            memory.set_app(t)