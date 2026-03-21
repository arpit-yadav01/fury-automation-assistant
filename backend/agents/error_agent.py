# agents/error_agent.py

from agents.base_agent import BaseAgent


class ErrorRecoveryAgent(BaseAgent):

    def __init__(self):
        super().__init__("ErrorRecoveryAgent")

    # -------------------------

    def can_handle(self, task):

        # error agent never auto handles
        return False

    # -------------------------

    def handle_error(self, task, error):

        print("ErrorRecoveryAgent handling error")

        print("Task:", task)
        print("Error:", error)

        # simple retry logic

        try:
            print("Retrying once...")
            return True
        except:
            print("Retry failed")
            return False