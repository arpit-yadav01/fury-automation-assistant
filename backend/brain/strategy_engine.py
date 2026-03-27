def build_strategy(goal_data):

    if not goal_data:
        return []

    goal = goal_data.get("goal")
    typ = goal_data.get("type")

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
                {"intent": "run_terminal", "command": "npx create-react-app myapp"}
            ]

    # -----------------------
    # INSTALL
    # -----------------------

    if goal == "install":

        steps = [
            {"intent": "run_terminal", "command": goal_data.get("raw")}
        ]

    return steps