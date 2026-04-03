from agents.base_agent import BaseAgent
from brain.task_understanding import understand_task


class TaskUnderstandingAgent(BaseAgent):

    def __init__(self):
        super().__init__("TaskUnderstandingAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("processed"):
            return False

        return task.get("intent") == "unknown"

    def handle(self, task):

        text = task.get("raw")

        if not text:
            return task

        data = understand_task(text)

        # ❌ fallback FIX (CRITICAL)
        if not data or not data.get("goal"):

            # 🔥 simple rule-based fallback
            text = text.lower()

            if "notepad" in text:
                return {
                    "intent": "open_app",
                    "app": "notepad"
                }

            if "type" in text:
                return {
                    "intent": "type_text",
                    "text": text.replace("type", "").strip()
                }

            return task

        # ✅ normal flow
        return {
            "intent": "goal_task",
            "data": data,
            "raw": text,
            "processed": True
        }