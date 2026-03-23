# agents/code_agent.py

from agents.base_agent import BaseAgent

from developer.code_generator import generate_code


class CodeAgent(BaseAgent):

    def __init__(self):
        super().__init__("CodeAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("intent") == "generate_code":
            return True

        return False

    # -------------------------

    def handle(self, task):

        lang = task.get("language", "python")
        t = task.get("task", "")

        print("CodeAgent generating code")

        code = generate_code(lang, t)

        print(code)

        return code