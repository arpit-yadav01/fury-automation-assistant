from execution.task_planner import create_plan
from execution.executor import execute_plan

from brain.context_memory import memory


# -----------------------------
# PRINT MEMORY
# -----------------------------

def show_memory():

    print("---- MEMORY ----")

    print("App:", memory.get_app())
    print("Window:", memory.get_window())
    print("Site:", memory.get_site())
    print("File:", memory.get_file())
    print("Action:", memory.get_action())

    print("----------------")


# -----------------------------
# MAIN LOOP
# -----------------------------

def start_fury():

    print("=================================")
    print("🔥 FURY AI ASSISTANT STARTED")
    print("Type 'exit' to stop Fury")
    print("=================================")

    while True:

        command = input(">>> ").strip()

        if not command:
            continue

        if command.lower() == "exit":
            print("Shutting down Fury...")
            break

        # -------------------------
        # CREATE PLAN
        # -------------------------

        plan = create_plan(command)

        print("\nExecution Plan:")

        if isinstance(plan, dict):
            print(plan)
        else:
            for step in plan:
                print(step)

        print()

        # -------------------------
        # EXECUTE
        # -------------------------

        execute_plan(plan)

        # -------------------------
        # SHOW MEMORY
        # -------------------------

        show_memory()

        print()


# -----------------------------

if __name__ == "__main__":
    start_fury()