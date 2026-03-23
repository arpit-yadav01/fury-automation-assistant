# agents/text_agent.py

from agents.base_agent import BaseAgent

from brain.llm_brain import interpret_with_llm


class TextAgent(BaseAgent):

    def __init__(self):
        super().__init__("TextAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("intent") == "generate_text":
            return True

        if task.get("text_llm"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        command = task.get("command")

        if not command:
            return

        print("TextAgent → LLM")

        result = interpret_with_llm(command)

        print(result)

        return result