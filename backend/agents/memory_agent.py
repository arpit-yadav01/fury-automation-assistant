# agents/memory_agent.py

from agents.base_agent import BaseAgent
from brain.context_memory import memory


class MemoryAgent(BaseAgent):

    def __init__(self):
        super().__init__("MemoryAgent")

    # -------------------------

    def can_handle(self, task):

        if isinstance(task, dict) and task.get("memory"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        data = task.get("memory")

        if not data:
            return

        if "app" in data:
            memory.set_app(data["app"])

        if "window" in data:
            memory.set_window(data["window"])

        if "site" in data:
            memory.set_site(data["site"])

        if "file" in data:
            memory.set_file(data["file"])

        if "action" in data:
            memory.set_action(data["action"])