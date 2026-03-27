from agents.base_agent import BaseAgent
from execution.error_solver import solve_error


class ErrorFixAgent(BaseAgent):

    def __init__(self):
        super().__init__("ErrorFixAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("intent") == "error":
            return True

        return False

    def handle(self, task):

        error = task.get("error")
        original_task = task.get("task")

        fix = solve_error(error, original_task)

        if not fix:
            print("No fix found")
            return

        print("Suggested fix:", fix)

        return fix