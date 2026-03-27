from agents.base_agent import BaseAgent
from execution.retry_engine import optimize_retry


class RetryAgent(BaseAgent):

    def __init__(self):
        super().__init__("RetryAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "retry"

    def handle(self, task):

        new_task = optimize_retry(
            task.get("task"),
            task.get("error")
        )

        print("Retry optimized:", new_task)

        return new_task