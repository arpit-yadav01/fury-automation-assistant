# execution/auto_loop.py

from execution.task_planner import create_plan
from execution.executor import execute_plan

from brain.context_memory import memory


MAX_STEPS = 5


def run_autonomous(command):

    print("AUTO MODE:", command)

    step = 0

    while step < MAX_STEPS:

        print("\nAUTO STEP:", step + 1)

        plan = create_plan(command)

        if not plan:
            print("No plan")
            break

        execute_plan(plan)

        memory.set_action("auto_step")

        step += 1

    print("AUTO LOOP FINISHED")