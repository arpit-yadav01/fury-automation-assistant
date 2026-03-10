# execution/task_planner.py

from brain.command_parser import parse_command
from brain.llm_brain import interpret_with_llm


def create_plan(command):

    tasks = []

    # Split commands like: "open youtube and search music"
    parts = command.split(" and ")

    for part in parts:

        part = part.strip()

        # 1️⃣ Try rule-based parser first
        task = parse_command(part)

        if task["intent"] != "unknown":

            tasks.append(task)

        else:

            # 2️⃣ Fallback to LLM reasoning
            llm_tasks = interpret_with_llm(part)

            if llm_tasks:
                tasks.extend(llm_tasks)

            else:
                tasks.append({"intent": "unknown"})

    return tasks