from agents.base_agent import BaseAgent
from core.thinking_engine import think


class ThinkingAgent(BaseAgent):

    def __init__(self):
        super().__init__("ThinkingAgent")

    def can_handle(self, task):

        if isinstance(task, str):
            return True

        return False

    def handle(self, task):

        result = think(task)

        if result:
            print("Thinking → structured task")
            return result

        return task