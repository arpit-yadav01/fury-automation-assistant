# execution/goal_engine.py

from execution.task_planner import create_plan
from execution.executor import execute_plan

from brain.context_memory import memory


MAX_GOAL_STEPS = 8


def run_goal(goal):

    print("GOAL MODE:", goal)

    step = 0

    last_action = None

    while step < MAX_GOAL_STEPS:

        print("\nGOAL STEP:", step + 1)

        plan = create_plan(goal)

        if not plan:
            print("No plan")
            break

        execute_plan(plan)

        action = memory.get_action()

        # stop if nothing changed
        if action == last_action:
            print("No change, stopping goal")
            break

        last_action = action

        step += 1

    print("GOAL FINISHED")