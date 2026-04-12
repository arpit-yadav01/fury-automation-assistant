# agents/base_agent.py
# STEP 116 — confidence() method added
#
# Every agent now has a confidence() method.
# agent_controller calls it before handle() to decide
# whether to proceed, ask, or abort.

from brain.confidence_engine import score_task


class BaseAgent:

    def __init__(self, name):
        self.name = name

    def can_handle(self, task):
        """
        Return True if this agent can handle task.
        """
        return False

    def confidence(self, task):
        """
        Score how confident this agent is about handling the task.

        Returns a result dict:
        {
            "score": float,       # 0.0 to 1.0
            "decision": str,      # "proceed" | "ask" | "abort"
            "reason": str,
            "risky": bool
        }

        Agents can override this for custom scoring logic.
        Default uses confidence_engine rule + LLM scoring.
        """
        return score_task(task)

    def handle(self, task):
        """
        Execute task. Must be implemented by subclass.
        """
        raise NotImplementedError