# agents/rag_memory_agent.py

from agents.base_agent import BaseAgent

from memory.memory_db import memory_db
from memory.json_memory import load_memory


class RAGMemoryAgent(BaseAgent):

    def __init__(self):
        super().__init__("RAGMemoryAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("rag_memory"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        print("RAGMemoryAgent")

        history = memory_db.get_history()

        data = load_memory()

        return {
            "history": history,
            "json": data,
        }