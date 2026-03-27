from agents.base_agent import BaseAgent
from memory.experience_db import experience_db


class ExperienceAgent(BaseAgent):

    def __init__(self):
        super().__init__("ExperienceAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "experience_add"

    def handle(self, task):

        experience_db.add(
            task.get("task"),
            task.get("action"),
            task.get("result"),
            task.get("success", 1)
        )

        print("Experience saved")