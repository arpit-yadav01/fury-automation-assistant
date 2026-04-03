from agents.base_agent import BaseAgent
from core.thinking_engine import think


class ThinkingAgent(BaseAgent):

    def __init__(self):
        super().__init__("ThinkingAgent")

    # -------------------------

    def can_handle(self, task):

        # ONLY handle raw string input
        if isinstance(task, str):
            return True

        # DO NOT block dict tasks (CRITICAL FIX)
        return False

    # -------------------------

    def handle(self, task):

        result = think(task)

        if result:
            print("Thinking → structured task")
            return result

        # 🔥 IMPORTANT: fallback to planner
        return {
            "intent": "parse_command",
            "text": task
        }