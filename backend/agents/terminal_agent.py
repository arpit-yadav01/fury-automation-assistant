# agents/terminal_agent.py

from agents.base_agent import BaseAgent

from developer.terminal_engine import run_terminal_command
from developer.dev_workflow import (
    open_vscode,
    create_new_file,
    write_code,
    save_file,
    run_python_file,
    run_command,
)


class TerminalAgent(BaseAgent):

    def __init__(self):
        super().__init__("TerminalAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        action = task.get("action")
        intent = task.get("intent")

        if action == "terminal":
            return True

        if intent in [
            "run_terminal",
            "open_vscode",
            "create_code_file",
            "write_code",
            "save_file",
            "run_python",
            "run_dev_command",
        ]:
            return True

        return False

    # -------------------------

    def handle(self, task):

        action = task.get("action")
        intent = task.get("intent")

        # workflow action

        if action == "terminal":

            cmd = task.get("cmd")

            run_terminal_command(cmd)

            return

        # intents

        if intent == "run_terminal":

            run_terminal_command(task.get("command"))
            return

        if intent == "open_vscode":
            open_vscode()
            return

        if intent == "create_code_file":
            create_new_file(task.get("filename"))
            return

        if intent == "write_code":
            write_code(task.get("code"))
            return

        if intent == "save_file":
            save_file()
            return

        if intent == "run_python":
            run_python_file(task.get("filename"))
            return

        if intent == "run_dev_command":
            run_command(task.get("command"))
            return