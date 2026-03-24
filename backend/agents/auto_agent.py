# agents/auto_agent.py

from agents.base_agent import BaseAgent

from execution.auto_mode_v2 import run_auto_v2


class AutoAgent(BaseAgent):

    def __init__(self):
        super().__init__("AutoAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("auto_v2"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        tasks = task.get("tasks")

        if not tasks:
            return

        run_auto_v2(tasks)