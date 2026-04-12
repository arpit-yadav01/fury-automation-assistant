# from agents.base_agent import BaseAgent

# from execution.executor import execute_plan
# from execution.workflow_engine import run_workflow
# from skills.skill_manager import execute_skill
# from skills.skills_registry import SKILLS


# class ExecutorAgent(BaseAgent):

#     def __init__(self):
#         super().__init__("ExecutorAgent")

#     # -------------------------

#     def can_handle(self, task):

#         if not isinstance(task, dict):
#             return False

#         # workflow
#         if "workflow" in task:
#             return True

#         # step
#         if task.get("action"):
#             return True

#         # ✅ ONLY HANDLE VALID SKILLS
#         if task.get("intent") in SKILLS:
#             return True

#         return False

#     # -------------------------

#     def handle(self, task):

#         # -------------------------
#         # WORKFLOW
#         # -------------------------

#         if "workflow" in task:

#             print("ExecutorAgent → workflow")

#             run_workflow(task["workflow"])

#             return

#         # -------------------------
#         # SINGLE STEP
#         # -------------------------

#         if task.get("action"):

#             print("ExecutorAgent → step")

#             run_workflow([task])

#             return

#         # -------------------------
#         # SKILL EXECUTION
#         # -------------------------

#         intent = task.get("intent")

#         if intent in SKILLS:

#             print("ExecutorAgent → skill:", intent)

#             success = execute_skill(intent, task)

#             if isinstance(success, dict):
#                 return success

#             return

#         # -------------------------
#         # FALLBACK
#         # -------------------------

#         print("ExecutorAgent → fallback")

#         execute_plan(task)


# agents/executor_agent.py
# FIX: execute_skill(task) takes 1 arg, not 2

from agents.base_agent import BaseAgent
from execution.executor import execute_plan
from execution.workflow_engine import run_workflow
from skills.skill_manager import execute_skill
from skills.skills_registry import SKILLS


class ExecutorAgent(BaseAgent):

    def __init__(self):
        super().__init__("ExecutorAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if "workflow" in task:
            return True

        if task.get("action"):
            return True

        if task.get("intent") in SKILLS:
            return True

        return False

    # -------------------------

    def handle(self, task):

        # -------------------------
        # WORKFLOW
        # -------------------------

        if "workflow" in task:
            print("ExecutorAgent → workflow")
            run_workflow(task["workflow"])
            return

        # -------------------------
        # SINGLE STEP
        # -------------------------

        if task.get("action"):
            print("ExecutorAgent → step")
            run_workflow([task])
            return

        # -------------------------
        # SKILL EXECUTION
        # FIX: was execute_skill(intent, task) — wrong, takes only task
        # -------------------------

        intent = task.get("intent")

        if intent in SKILLS:
            print("ExecutorAgent → skill:", intent)
            success = execute_skill(task)          # ✅ fixed: task only
            if isinstance(success, dict):
                return success
            return

        # -------------------------
        # FALLBACK
        # -------------------------

        print("ExecutorAgent → fallback")
        execute_plan(task)