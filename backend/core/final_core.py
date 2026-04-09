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

# step 107
from brain.context_engine import enrich_command

# step 110
from brain.personality import respond


class FinalCore:

    def __init__(self):
        pass

    def execute(self, command):

        print(respond("executing"))

        # ✅ STEP 107 — enrich vague commands
        command = enrich_command(command)

        # ✅ STEP 1 — build plan
        plan = create_plan(command)

        print(f"FinalCore → plan type: {type(plan)}")

        # ✅ STEP 2 — execute
        if isinstance(plan, dict) and "workflow" in plan:
            print("FinalCore → running workflow directly")
            run_workflow(plan["workflow"])
        else:
            controller.execute(plan)

        # ✅ STEP 3 — save experience
        try:
            save_experience(command, plan, result=True)
        except Exception as e:
            print("Experience save failed:", e)

        print(respond("learn"))

        self.after_step()

        print(respond("done"))

        # pattern debug
        try:
            patterns = get_frequent_command()
            if patterns:
                print("📊 Frequent actions:", patterns[:2])
        except:
            pass

    def after_step(self):
        self_improve.improve()

    def save_state(self):
        session_db.save("last", "ok")


final_core = FinalCore()