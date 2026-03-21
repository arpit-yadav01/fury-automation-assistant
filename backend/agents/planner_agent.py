# agents/planner_agent.py

from agents.base_agent import BaseAgent

from execution.task_planner import create_plan


class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("PlannerAgent")

    # -------------------------

    def can_handle(self, task):

        # Planner handles raw text command

        if isinstance(task, str):
            return True

        if isinstance(task, dict) and task.get("intent") == "plan":
            return True

        return False

    # -------------------------

    def handle(self, task):

        if isinstance(task, str):

            print("PlannerAgent → create_plan")

            plan = create_plan(task)

            return plan

        if isinstance(task, dict):

            command = task.get("command")

            if command:

                plan = create_plan(command)

                return plan

        return None