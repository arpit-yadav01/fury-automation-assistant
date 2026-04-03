from agents.base_agent import BaseAgent
from planner.ui_action_planner import plan_ui_actions


class UIPlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("UIPlannerAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "web_search"

    def handle(self, task):

        actions = plan_ui_actions(task)

        if not actions:
            return task

        print("UIPlannerAgent → actions:", actions)

        # ✅ CRITICAL FIX: convert to workflow
        return {
            "intent": "workflow",
            "workflow": [
                {"intent": "ui_action", "data": action}
                for action in actions
            ]
        }
    



class UIPlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("UIPlannerAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "ui_goal"

    def handle(self, task):

        goal = task.get("goal", "")

        print("UIPlannerAgent → planning:", goal)

        # simple example
        if "search" in goal:

            return {
                "intent": "ui_action_sequence",
                "data": [
                    {"action": "click"},
                    {"action": "type", "text": goal.replace("search", "").strip()},
                    {"action": "enter"}
                ]
            }

        return None    