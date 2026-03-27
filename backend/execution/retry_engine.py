def optimize_retry(task, error):

    if not task:
        return task

    text = str(error).lower()

    if "not found" in text:

        name = task.get("name", "")

        if name:
            return {
                "intent": "run_terminal",
                "command": f"pip install {name}"
            }

    if "timeout" in text:

        return {
            "intent": "wait",
            "time": 3
        }

    return task