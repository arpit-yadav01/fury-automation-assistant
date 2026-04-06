# core/final_core.py

from agents.agent_controller import controller
from core.self_improve import self_improve
from memory.session_db import session_db

# ✅ STEP 102
from memory.experience_memory import save_experience


class FinalCore:

    def __init__(self):
        pass

    # -----------------

    def execute(self, plan):

        # -----------------
        # EXECUTE PLAN
        # -----------------

        controller.execute(plan)

        # -----------------
        # SAVE EXPERIENCE (SAFE)
        # -----------------

        try:
            command = None

            if isinstance(plan, dict):
                command = plan.get("raw") or plan.get("command") or str(plan)
            else:
                command = str(plan)

            save_experience(command, plan, result=True)

        except Exception as e:
            print("Experience save failed:", e)

        # -----------------

        self.after_step()

    # -----------------

    def after_step(self):

        self_improve.improve()

    # -----------------

    def save_state(self):

        session_db.save("last", "ok")


# global instance
final_core = FinalCore()