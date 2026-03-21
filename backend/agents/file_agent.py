# agents/file_agent.py

from agents.base_agent import BaseAgent

from automation.file_manager import (
    create_file,
    write_to_file,
)

from brain.context_memory import memory


class FileAgent(BaseAgent):

    def __init__(self):
        super().__init__("FileAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        action = task.get("action")
        intent = task.get("intent")

        if action == "create_file":
            return True

        if intent in [
            "create_file",
            "write_file",
        ]:
            return True

        return False

    # -------------------------

    def handle(self, task):

        action = task.get("action")
        intent = task.get("intent")

        # workflow action

        if action == "create_file":

            path = task.get("path")

            create_file(path)

            memory.set_file(path)

            return

        # intents

        if intent == "create_file":

            name = task.get("filename")

            create_file(name)

            memory.set_file(name)

            return

        if intent == "write_file":

            name = task.get("filename")
            text = task.get("text")

            write_to_file(name, text)

            memory.set_file(name)

            return