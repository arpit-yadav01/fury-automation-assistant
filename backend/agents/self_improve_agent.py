# agents/self_improve_agent.py

from agents.base_agent import BaseAgent

from core.self_improve import self_improve


class SelfImproveAgent(BaseAgent):

    def __init__(self):
        super().__init__("SelfImproveAgent")

    # -----------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("self_improve"):
            return True

        return False

    # -----------------

    def handle(self, task):

        self_improve.improve()