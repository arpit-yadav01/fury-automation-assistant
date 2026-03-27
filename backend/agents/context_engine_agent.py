from agents.base_agent import BaseAgent
from memory.context_engine import context_engine


class ContextEngineAgent(BaseAgent):

    def __init__(self):
        super().__init__("ContextEngineAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        # automatically track important tasks
        if task.get("intent") in ["goal_task", "workflow", "action"]:
            return True

        if task.get("intent") == "context_update":
            return True

        return False

    def handle(self, task):

        # track goal
        if task.get("intent") == "goal_task":

            data = task.get("data", {})
            context_engine.set_goal(data.get("goal"))

        # track step
        if task.get("intent") == "workflow":

            context_engine.set_step("workflow_running")

        # track history
        context_engine.add_history(task)

        return task