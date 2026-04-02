from agents.base_agent import BaseAgent
from execution.operator_loop import run_operator_loop


class OperatorAgent(BaseAgent):

    def __init__(self):
        super().__init__("OperatorAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "ui_action_sequence"

    def handle(self, task):

        actions = task.get("data", [])

        print("OperatorAgent → executing sequence")

        result = run_operator_loop(actions)

        return result