from agents.base_agent import BaseAgent
from vision.target_selector import select_best_target


class TargetSelectionAgent(BaseAgent):

    def __init__(self):
        super().__init__("TargetSelectionAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "select_target"

    def handle(self, task):

        objects = task.get("objects", [])

        best = select_best_target(objects)

        print("TargetSelectionAgent → selected:", best)

        return {
            "intent": "selected_target",
            "data": best
        }