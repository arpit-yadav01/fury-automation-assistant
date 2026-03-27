from agents.base_agent import BaseAgent

from execution.subtask_executor import execute_subtasks


class SubtaskAgent(BaseAgent):

    def __init__(self):
        super().__init__("SubtaskAgent")

    # -----------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("workflow"):
            return True

        return False

    # -----------------

    def handle(self, task):

        workflow = task.get("workflow")

        steps = execute_subtasks(workflow)

        if not steps:
            return task

        return {
            "intent": "workflow",
            "workflow": steps,
            "source": "subtask_executor",
        }