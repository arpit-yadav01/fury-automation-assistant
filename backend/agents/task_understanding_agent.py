from agents.base_agent import BaseAgent
from brain.task_understanding import understand_task


class TaskUnderstandingAgent(BaseAgent):

    def __init__(self):
        super().__init__("TaskUnderstandingAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        # prevent loop
        if task.get("processed"):
            return False

        return task.get("intent") == "unknown"

    def handle(self, task):

        text = task.get("raw")

        if not text:
            return task

        text_lower = text.lower()

        # =========================
        # 🔥 PHASE 7 — SMART UI ROUTING
        # =========================

        if "youtube" in text_lower and "search" in text_lower:

            query = text_lower.split("search")[-1].strip()

            return {
                "intent": "ui_goal",
                "goal": f"search {query}",
                "platform": "youtube",
                "raw": text,
                "processed": True,
            }

        # =========================
        # NORMAL UNDERSTANDING
        # =========================

        data = understand_task(text)

        # fallback safe exit
        if not data or not data.get("goal"):
            return {
                "intent": "text",
                "raw": text
            }

        return {
            "intent": "goal_task",
            "data": data,
            "raw": text,
            "processed": True
        }