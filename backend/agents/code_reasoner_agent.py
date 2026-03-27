from agents.base_agent import BaseAgent
from developer.code_analyzer import analyze_code
from developer.code_fixer import fix_code


class CodeReasonerAgent(BaseAgent):

    def __init__(self):
        super().__init__("CodeReasonerAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("intent") in ["analyze_code", "fix_code"]:
            return True

        return False

    def handle(self, task):

        intent = task.get("intent")

        if intent == "analyze_code":

            code = task.get("code")

            result = analyze_code(code)

            print("Code Analysis:", result)

            return result

        if intent == "fix_code":

            code = task.get("code")

            fixed = fix_code(code)

            print("Fixed Code:\n", fixed)

            return {
                "intent": "code_fixed",
                "code": fixed
            }