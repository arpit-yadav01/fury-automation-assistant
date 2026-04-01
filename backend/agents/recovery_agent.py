from agents.base_agent import BaseAgent
from execution.recovery_engine import recover_action


class RecoveryAgent(BaseAgent):

    def __init__(self):
        super().__init__("RecoveryAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "recover"

    def handle(self, task):

        action = task.get("action")
        attempt = task.get("attempt", 0)

        new_action = recover_action(action, attempt)

        print("RecoveryAgent →", new_action)

        return new_action