# agents/session_agent.py

from agents.base_agent import BaseAgent

from memory.session_db import session_db


class SessionAgent(BaseAgent):

    def __init__(self):
        super().__init__("SessionAgent")

    # -----------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("session"):
            return True

        return False

    # -----------------

    def handle(self, task):

        mode = task.get("session")

        if mode == "save":

            session_db.save(
                task.get("key"),
                str(task.get("value")),
            )

        if mode == "load":

            return session_db.load_all()