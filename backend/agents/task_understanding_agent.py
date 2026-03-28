from agents.base_agent import BaseAgent
from brain.task_understanding import understand_task


class TaskUnderstandingAgent(BaseAgent):

    def __init__(self):
        super().__init__("TaskUnderstandingAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        # ✅ prevent infinite loop
        if task.get("processed"):
            return False

        return task.get("intent") == "unknown"

    def handle(self, task):

        text = task.get("raw")

        if not text:
            return task

        data = understand_task(text)

        # ❌ if nothing understood → STOP loop safely
        if not data or not data.get("goal"):
            return {
                "intent": "text",
                "raw": text
            }

        # ✅ convert to goal task
        return {
            "intent": "goal_task",
            "data": data,
            "raw": text,
            "processed": True
        }