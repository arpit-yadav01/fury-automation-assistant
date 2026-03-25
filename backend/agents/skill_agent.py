# # agents/skill_agent.py

# from agents.base_agent import BaseAgent

# from skills.skill_manager import execute_skill


# class SkillAgent(BaseAgent):

#     def __init__(self):
#         super().__init__("SkillAgent")

#     # -------------------------

#     def can_handle(self, task):

#         if not isinstance(task, dict):
#             return False

#         if task.get("intent"):
#             return True

#         return False

#     # -------------------------

#     def handle(self, task):

#         intent = task.get("intent")

#         if not intent:
#             return

#         ok = execute_skill(task)

#         if not ok:
#             raise Exception("Skill failed")


from agents.base_agent import BaseAgent
from skills.skill_manager import execute_skill


class SkillAgent(BaseAgent):

    def __init__(self):
        super().__init__("SkillAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        intent = task.get("intent")

        if not intent:
            return False

        # FIX-2 do not steal code
        if intent == "generate_code":
            return False

        # do not steal dev
        if intent == "dev":
            return False

        return True

    def handle(self, task):

        ok = execute_skill(task)

        if not ok:
            raise Exception("Skill failed")