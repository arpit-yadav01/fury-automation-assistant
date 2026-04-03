# agents/planner_agent.py

from agents.base_agent import BaseAgent
from execution.task_planner import create_plan


class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("PlannerAgent")

    # -------------------------

    def can_handle(self, task):

        # ✅ ONLY handle raw user input
        if isinstance(task, str):
            return True

        # ✅ explicit planning request only
        if isinstance(task, dict) and task.get("intent") == "plan":
            return True

        # ❌ DO NOT touch structured pipeline
        return False

    # -------------------------

    def handle(self, task):

        # -------------------------
        # RAW STRING → PLAN
        # -------------------------

        if isinstance(task, str):

            print("PlannerAgent → create_plan")

            plan = create_plan(task)

            return plan

        # -------------------------
        # EXPLICIT PLAN REQUEST
        # -------------------------

        if isinstance(task, dict):

            command = task.get("command")

            if command:
                print("PlannerAgent → plan from dict")

                plan = create_plan(command)

                return plan

        return None