# agents/context_agent.py

from agents.base_agent import BaseAgent

from automation.window_manager import (
    get_active_window_title,
)

from brain.context_memory import memory


class ContextTrackingAgent(BaseAgent):

    def __init__(self):
        super().__init__("ContextTrackingAgent")

    # -------------------------

    def can_handle(self, task):

        if isinstance(task, dict) and task.get("context_check"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        title = get_active_window_title()

        if not title:
            return

        title_low = title.lower()

        print("ContextAgent →", title)

        memory.set_window(title)

        if "chrome" in title_low:
            memory.set_app("browser")

        elif "code" in title_low:
            memory.set_app("vscode")

        elif "notepad" in title_low:
            memory.set_app("notepad")

        elif "cmd" in title_low or "powershell" in title_low:
            memory.set_app("terminal")

        else:
            memory.set_app(title_low)