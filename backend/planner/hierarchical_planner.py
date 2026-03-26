def build_goal_plan(data):

    if not isinstance(data, dict):
        return []

    goal = data.get("goal")
    typ = data.get("type")
    raw = data.get("raw")

    steps = []

    # -----------------------
    # BUILD PROJECT
    # -----------------------

    if goal == "build":

        if typ == "python":

            steps = [
                {"intent": "open_app", "app": "vscode"},
                {"intent": "create_file", "filename": "main.py"},
                {"intent": "type_text", "text": "print('hello')"},
            ]

        elif typ == "react":

            steps = [
                {
                    "intent": "run_terminal",
                    "command": "npx create-react-app myapp",
                }
            ]

        elif typ == "node":

            steps = [
                {
                    "intent": "run_terminal",
                    "command": "npm init -y",
                }
            ]

    # -----------------------
    # INSTALL
    # -----------------------

    elif goal == "install":

        if raw:

            steps = [
                {
                    "intent": "run_terminal",
                    "command": raw,
                }
            ]

    # -----------------------
    # SOLVE
    # -----------------------

    elif goal == "solve":

        steps = [
            {
                "intent": "text",
                "text": raw,
            }
        ]

    return steps