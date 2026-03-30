from agents.base_agent import BaseAgent
from automation.ui_action_engine import perform_ui_action


class UIActionAgent(BaseAgent):

    def __init__(self):
        super().__init__("UIActionAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "ui_action"

    def handle(self, task):

        action = task.get("data")

        if not action:
            print("UIActionAgent → no action provided")
            return None

        print("UIActionAgent →", action)

        result = perform_ui_action(action)

        return result