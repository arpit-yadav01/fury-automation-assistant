# agents/skill_agent.py

from agents.base_agent import BaseAgent

from skills.skill_manager import execute_skill


class SkillAgent(BaseAgent):

    def __init__(self):
        super().__init__("SkillAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("intent"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        intent = task.get("intent")

        if not intent:
            return

        ok = execute_skill(task)

        if not ok:
            raise Exception("Skill failed")