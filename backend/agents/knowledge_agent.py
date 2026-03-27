from agents.base_agent import BaseAgent

from memory.knowledge_db import knowledge_db


class KnowledgeAgent(BaseAgent):

    def __init__(self):
        super().__init__("KnowledgeAgent")

    # -----------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("intent") == "knowledge_add":
            return True

        if task.get("intent") == "knowledge_get":
            return True

        return False

    # -----------------

    def handle(self, task):

        intent = task.get("intent")

        if intent == "knowledge_add":

            knowledge_db.add(
                task.get("key"),
                task.get("value"),
            )

            print("Knowledge saved")

            return

        if intent == "knowledge_get":

            value = knowledge_db.get(
                task.get("key")
            )

            print("Knowledge:", value)

            return value