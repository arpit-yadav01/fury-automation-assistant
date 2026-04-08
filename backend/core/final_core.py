# # core/final_core.py

# from agents.agent_controller import controller
# from core.self_improve import self_improve
# from memory.session_db import session_db

# # ✅ STEP 102
# from memory.experience_memory import save_experience
# from brain.pattern_engine import get_frequent_command

# class FinalCore:

#     def __init__(self):
#         pass

#     # -----------------

#     def execute(self, plan):

#         # -----------------
#         # EXECUTE PLAN
#         # -----------------

#         controller.execute(plan)

#         # -----------------
#         # SAVE EXPERIENCE (SAFE)
#         # -----------------

#         try:
#             command = None

#             if isinstance(plan, dict):
#                 command = plan.get("raw") or plan.get("command") or str(plan)
#             else:
#                 command = str(plan)

#             save_experience(command, plan, result=True)

#         except Exception as e:
#             print("Experience save failed:", e)

#         # -----------------

#         self.after_step()

#     # -----------------

#     def after_step(self):

#         self_improve.improve()

#     # -----------------

#     def save_state(self):

#         session_db.save("last", "ok")


    

# patterns = get_frequent_command()

# if patterns:
#     print("📊 Frequent actions:", patterns[:2])

# # global instance
# final_core = FinalCore()


from agents.agent_controller import controller
from core.self_improve import self_improve
from memory.session_db import session_db

from memory.experience_memory import save_experience
from brain.pattern_engine import get_frequent_command

from execution.task_planner import create_plan
from execution.workflow_engine import run_workflow


class FinalCore:

    def __init__(self):
        pass

    # -----------------

    def execute(self, command):

        # =========================
        # STEP 1 — BUILD PLAN
        # =========================

        plan = create_plan(command)

        print("FinalCore → plan type:", type(plan))

        # =========================
        # STEP 2 — EXECUTE SAFELY
        # =========================

        if isinstance(plan, dict) and "workflow" in plan:

            print("FinalCore → running workflow directly")

            run_workflow(plan["workflow"])

        else:

            controller.execute(plan)

        # =========================
        # STEP 3 — SAVE EXPERIENCE
        # =========================

        try:
            save_experience(command, plan, result=True)
        except Exception as e:
            print("Experience save failed:", e)

        # =========================

        self.after_step()

        # =========================
        # STEP 4 — PATTERN DEBUG
        # =========================

        patterns = get_frequent_command()

        if patterns:
            print("📊 Frequent actions:", patterns[:2])

    # -----------------

    def after_step(self):
        self_improve.improve()

    # -----------------

    def save_state(self):
        session_db.save("last", "ok")


# global
final_core = FinalCore()