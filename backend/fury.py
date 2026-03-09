from execution.task_planner import create_plan
from execution.executor import execute_plan


def start_fury():

    print("=================================")
    print("🔥 FURY AI ASSISTANT STARTED")
    print("Type 'exit' to stop Fury")
    print("=================================")

    while True:

        command = input(">>> ")

        if command.lower() == "exit":
            print("Shutting down Fury...")
            break

        plan = create_plan(command)

        print("Execution Plan:")

        for step in plan:
            print(step)

        execute_plan(plan)


if __name__ == "__main__":
    start_fury()