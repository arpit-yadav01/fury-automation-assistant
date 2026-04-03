# agents/planner_agent.py

from agents.base_agent import BaseAgent
from execution.task_planner import create_plan


class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("PlannerAgent")

    # -------------------------

    def can_handle(self, task):

        # ✅ handle raw user input
        if isinstance(task, str):
            return True

        # ✅ explicit planning request
        if isinstance(task, dict) and task.get("intent") == "plan":
            return True

        return False

    # -------------------------

    def handle(self, task):

        # =========================
        # CASE 1 — RAW USER INPUT
        # =========================

        if isinstance(task, str):

            print("PlannerAgent → create_plan")

            # 🔥 MULTI-COMMAND SUPPORT
            if " and " in task:

                parts = task.split(" and ")

                return [
                    create_plan(part.strip())
                    for part in parts
                ]

            return create_plan(task)

        # =========================
        # CASE 2 — DICT PLAN REQUEST
        # =========================

        if isinstance(task, dict):

            command = task.get("command")

            if command:

                print("PlannerAgent → plan from dict")

                # 🔥 MULTI-COMMAND SUPPORT
                if " and " in command:

                    parts = command.split(" and ")

                    return [
                        create_plan(part.strip())
                        for part in parts
                    ]

                return create_plan(command)

        return None