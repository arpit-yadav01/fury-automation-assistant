# core/self_improve.py

from memory.memory_db import memory_db
from memory.skill_db import skill_db


class SelfImprove:

    def __init__(self):
        pass

    # -----------------

    def learn_from_history(self):

        history = memory_db.get_history()

        for h in history:

            command, action, result = h

            if not action:
                continue

            name = command

            data = {
                "action": action,
                "result": result,
            }

            skill_db.save_skill(name, str(data))

        print("SelfImprove: learned from history")

    # -----------------

    def improve(self):

        self.learn_from_history()


self_improve = SelfImprove()