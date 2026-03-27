from agents.base_agent import BaseAgent
from brain.task_understanding import understand_task


class TaskUnderstandingAgent(BaseAgent):

    def __init__(self):
        super().__init__("TaskUnderstandingAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        # only handle unknown intent
        if task.get("intent") == "unknown":
            return True

        return False

    def handle(self, task):

        text = task.get("raw")

        if not text:
            return task

        data = understand_task(text)

        if not data:
            return task

        if not data.get("goal"):
            return task

        # IMPORTANT: keep raw
        return {
            "intent": "goal_task",
            "data": data,
            "raw": text,
        }