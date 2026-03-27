from brain.task_understanding import understand_task


def think(text):

    if not text:
        return None

    data = understand_task(text)

    if not data or not data.get("goal"):
        return None

    return {
        "intent": "goal_task",
        "data": data
    }