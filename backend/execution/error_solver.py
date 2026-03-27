def solve_error(error, task):

    if not error:
        return None

    text = str(error).lower()

    # -----------------------
    # COMMON FIXES
    # -----------------------

    if "not found" in text:

        name = ""
        if isinstance(task, dict):
            name = task.get("name") or ""

        if name:
            return {
                "intent": "run_terminal",
                "command": f"pip install {name}"
            }

    if "permission" in text:

        return {
            "intent": "run_terminal",
            "command": "run as administrator"
        }

    return None