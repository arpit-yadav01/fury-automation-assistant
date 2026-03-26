from agents.base_agent import BaseAgent
from planner.hierarchical_planner import build_goal_plan


class AdvancedPlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("AdvancedPlannerAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("intent") == "goal_task":
            return True

        return False

    def handle(self, task):

        data = task.get("data")

        steps = build_goal_plan(data)

        if not steps:
            return task

        return {
            "intent": "workflow",
            "workflow": steps,
            "source": "advanced_planner",
        }