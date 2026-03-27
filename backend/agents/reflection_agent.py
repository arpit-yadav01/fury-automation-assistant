from agents.base_agent import BaseAgent
from core.reflection import reflect


class ReflectionAgent(BaseAgent):

    def __init__(self):
        super().__init__("ReflectionAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "reflect"

    def handle(self, task):

        summary = reflect(
            task.get("task"),
            task.get("success", True)
        )

        print("Reflection:", summary)

        return summary