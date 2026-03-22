# agents/api_agent.py

from agents.base_agent import BaseAgent

from brain.llm_brain import interpret_with_llm
from brain.ai_interpreter import interpret_command


class APIAgent(BaseAgent):

    def __init__(self):
        super().__init__("APIAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("use_llm"):
            return True

        if task.get("use_ai"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        command = task.get("command")

        if not command:
            return None

        # AI interpreter first

        if task.get("use_ai"):

            print("APIAgent → ai_interpreter")

            result = interpret_command(command)

            if result:
                return result

        # LLM fallback

        if task.get("use_llm"):

            print("APIAgent → llm")

            result = interpret_with_llm(command)

            if result:
                return result

        return None