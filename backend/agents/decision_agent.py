from agents.base_agent import BaseAgent
from brain.decision_engine import decide_action


class DecisionAgent(BaseAgent):

    def __init__(self):
        super().__init__("DecisionAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "decide"

    # ---------------------

    def handle(self, task):

        options = task.get("options")

        decision = decide_action(options)

        print("DecisionAgent →", decision)

        return decision