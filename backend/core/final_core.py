# core/final_core.py

from agents.agent_controller import controller

from core.self_improve import self_improve

from memory.session_db import session_db


class FinalCore:

    def __init__(self):
        pass

    # -----------------

    def execute(self, plan):

        controller.execute(plan)

        self.after_step()

    # -----------------

    def after_step(self):

        self_improve.improve()

    # -----------------

    def save_state(self):

        session_db.save("last", "ok")


final_core = FinalCore()