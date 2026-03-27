# execution/subtask_executor.py


def execute_subtasks(workflow):

    if not workflow:
        return []

    steps = []

    for step in workflow:

        if not isinstance(step, dict):
            continue

        # allow intent -> action conversion
        if "intent" in step and "action" not in step:
            step["action"] = step["intent"]

        steps.append(step)

    return steps