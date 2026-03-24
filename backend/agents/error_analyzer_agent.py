# agents/error_analyzer_agent.py

from agents.base_agent import BaseAgent

from core.message_bus import bus


class ErrorAnalyzerAgent(BaseAgent):

    def __init__(self):
        super().__init__("ErrorAnalyzerAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("error"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        print("ErrorAnalyzerAgent")

        error = task.get("error")
        last = task.get("last_task")

        print("Error:", error)

        decision = {
            "retry": False,
            "skip": False,
            "replan": False,
        }

        # simple logic

        if "not found" in str(error).lower():
            decision["retry"] = True

        elif "timeout" in str(error).lower():
            decision["retry"] = True

        else:
            decision["replan"] = True

        bus.send(
            "ErrorAnalyzer",
            "controller",
            decision,
        )

        return decision