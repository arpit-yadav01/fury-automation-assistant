# execution/task_planner.py

from brain.command_parser import parse_command


def create_plan(command):

    # Split commands by "and"
    parts = command.split(" and ")

    tasks = []

    for part in parts:
        task = parse_command(part.strip())
        tasks.append(task)

    return tasks 