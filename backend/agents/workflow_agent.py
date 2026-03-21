# agents/workflow_agent.py

from agents.base_agent import BaseAgent

from execution.workflow_engine import run_workflow


class WorkflowAgent(BaseAgent):

    def __init__(self):
        super().__init__("WorkflowAgent")

    # -------------------------

    def can_handle(self, task):

        if isinstance(task, dict) and "workflow" in task:
            return True

        if isinstance(task, dict) and task.get("action"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        if "workflow" in task:

            print("WorkflowAgent → run_workflow")

            run_workflow(task["workflow"])

            return

        if task.get("action"):

            print("WorkflowAgent → step")

            run_workflow([task])

            return