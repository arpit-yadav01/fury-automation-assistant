from agents.base_agent import BaseAgent
from memory.app_db import get_app


class AppIntelligenceAgent(BaseAgent):

    def __init__(self):
        super().__init__("AppIntelligenceAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "app_info"

    def handle(self, task):

        app = task.get("app")

        if not app:
            print("AppIntelligenceAgent → no app provided")
            return None

        data = get_app(app)

        print("App Intelligence:", data)

        return data