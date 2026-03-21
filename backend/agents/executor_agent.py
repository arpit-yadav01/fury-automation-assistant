# agents/executor_agent.py

from agents.base_agent import BaseAgent

from execution.executor import execute_plan
from execution.workflow_engine import run_workflow
from skills.skill_manager import execute_skill


class ExecutorAgent(BaseAgent):

    def __init__(self):
        super().__init__("ExecutorAgent")

    # -------------------------

    def can_handle(self, task):

        if isinstance(task, dict) and "workflow" in task:
            return True

        if isinstance(task, dict) and task.get("intent"):
            return True

        if isinstance(task, dict) and task.get("action"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        # workflow dict
        if isinstance(task, dict) and "workflow" in task:

            print("ExecutorAgent → workflow")

            run_workflow(task["workflow"])

            return

        # workflow step
        if isinstance(task, dict) and task.get("action"):

            print("ExecutorAgent → step")

            run_workflow([task])

            return

        # skill / intent
        if isinstance(task, dict) and task.get("intent"):

            print("ExecutorAgent → skill")

            execute_skill(task)

            return

        # fallback
        print("ExecutorAgent fallback")

        execute_plan(task)