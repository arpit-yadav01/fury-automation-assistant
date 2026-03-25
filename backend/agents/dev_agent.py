from agents.base_agent import BaseAgent

from developer.dev_workflow import (
    open_vscode,
    create_new_file,
    write_code,
    save_file,
    run_python_file,
    run_command,
)


class DevAgent(BaseAgent):

    def __init__(self):
        super().__init__("DevAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("dev"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        cmd = task.get("dev")

        if cmd == "open_vscode":
            open_vscode()
            return

        if cmd == "new_file":
            create_new_file(task.get("name", "test.py"))
            return

        if cmd == "write":
            write_code(task.get("code", ""))
            return

        if cmd == "save":
            save_file()
            return

        if cmd == "run":
            run_python_file(task.get("name", "test.py"))
            return

        if cmd == "command":
            run_command(task.get("cmd", ""))
            return