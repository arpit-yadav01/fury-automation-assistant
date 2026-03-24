# agents/final_core_agent.py

from agents.base_agent import BaseAgent

from core.final_core import final_core


class FinalCoreAgent(BaseAgent):

    def __init__(self):
        super().__init__("FinalCoreAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("final"):
            return True

        return False

    def handle(self, task):

        final_core.after_step()