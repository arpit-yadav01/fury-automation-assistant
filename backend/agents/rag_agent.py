# agents/rag_agent.py

from agents.base_agent import BaseAgent

from brain.context_memory import memory


class RAGAgent(BaseAgent):

    def __init__(self):
        super().__init__("RAGAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("rag"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        print("RAGAgent → memory lookup")

        data = {
            "app": memory.get_app(),
            "window": memory.get_window(),
            "site": memory.get_site(),
            "file": memory.get_file(),
            "action": memory.get_action(),
        }

        print("RAG:", data)

        return data