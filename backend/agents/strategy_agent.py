from agents.base_agent import BaseAgent


class StrategyAgent(BaseAgent):

    def __init__(self):
        super().__init__("StrategyAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "goal_task"

    def handle(self, task):

        data = task.get("data", {})

        goal = data.get("goal")
        typ = data.get("type")

        steps = []

        # -----------------------
        # BUILD PROJECT
        # -----------------------

        if goal == "build":

            if typ == "python":

                steps = [
                    {"intent": "open_app", "app": "code"},
                    {"intent": "create_file", "filename": "main.py"},
                    {"intent": "type_text", "text": "print('Hello World')"},
                ]

            elif typ == "react":

                steps = [
                    {
                        "intent": "run_terminal",
                        "command": "npx create-react-app myapp"
                    }
                ]

        # -----------------------
        # INSTALL PACKAGE
        # -----------------------

        if goal == "install":

            name = data.get("name", "")

            if name:
                steps = [
                    {
                        "intent": "run_terminal",
                        "command": f"pip install {name}"
                    }
                ]

        # -----------------------
        # ANALYZE UI
        # -----------------------

        if goal == "analyze_ui":

            steps = [
                {"intent": "analyze_ui"}
            ]

        # -----------------------

        print("Strategy built:", len(steps), "steps")

        return {
            "workflow": steps
        }