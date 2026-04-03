from agents.base_agent import BaseAgent
from automation.navigation_engine import navigate_and_click


class NavigationAgent(BaseAgent):

    def __init__(self):
        super().__init__("NavigationAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "auto_navigate"

    def handle(self, task):

        keyword = task.get("keyword")

        print("NavigationAgent → goal-based navigation:", keyword)

        success = navigate_and_click(keyword=keyword)

        return success