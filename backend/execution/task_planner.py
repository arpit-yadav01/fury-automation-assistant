# execution/task_planner.py

from brain.command_parser import parse_command
from brain.llm_brain import interpret_with_llm
from brain.ai_interpreter import interpret_command


def create_plan(command):

    # 1. Try AI interpreter first (whole sentence)
    ai_result = interpret_command(command)

    if ai_result:
        return [ai_result]

    # 2. Try LLM
    llm_tasks = interpret_with_llm(command)

    if llm_tasks:
        return llm_tasks

    # 3. Fallback to rule parser with split
    parts = command.split(" and ")

    tasks = []

    for part in parts:

        task = parse_command(part.strip())

        tasks.append(task)

    return tasks