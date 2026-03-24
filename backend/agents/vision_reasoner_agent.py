# agents/vision_reasoner_agent.py

from agents.base_agent import BaseAgent

from vision.ui_reasoner_v2 import (
    find_and_validate,
    exists,
)


class VisionReasonerAgent(BaseAgent):

    def __init__(self):
        super().__init__("VisionReasonerAgent")

    # -----------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("vision_reason"):
            return True

        return False

    # -----------------

    def handle(self, task):

        cmd = task.get("vision_reason")

        if cmd == "exists":

            text = task.get("text")

            return exists(text)

        if cmd == "find":

            text = task.get("text")

            return find_and_validate(text)