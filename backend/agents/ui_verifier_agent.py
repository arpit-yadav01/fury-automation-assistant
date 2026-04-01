from agents.base_agent import BaseAgent
from vision.ui_verifier import verify_action


class UIVerifierAgent(BaseAgent):

    def __init__(self):
        super().__init__("UIVerifierAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "verify_ui"

    def handle(self, task):

        before = task.get("before")
        after = task.get("after")

        result = verify_action(before, after)

        print("UIVerifier →", result)

        return result