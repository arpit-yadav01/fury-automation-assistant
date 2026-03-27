# execution/executor.py

from skills.skill_manager import execute_skill

from execution.workflow_engine import run_workflow

from brain.context_memory import memory


MAX_RETRY = 2


def execute_plan(plan):

    if not plan:
        print("No tasks to execute")
        return


    # -----------------------------
    # WORKFLOW SUPPORT
    # -----------------------------

    if isinstance(plan, dict) and "workflow" in plan:

        retry = 0

        while retry <= MAX_RETRY:

            try:

                print("Executing workflow")

                run_workflow(plan["workflow"])

                memory.set_action("workflow")

                return

            except Exception as e:

                print("Workflow error:", e)

                retry += 1

                print("Retry:", retry)

        print("Workflow failed")

        return


    # -----------------------------
    # PHASE 1 COMPATIBILITY
    # -----------------------------

    if isinstance(plan, dict):
        plan = [plan]


    for task in plan:

        if not isinstance(task, dict):
            print("Invalid task:", task)
            continue


        retry = 0

        while retry <= MAX_RETRY:

            executed = execute_skill(task)

            if executed:

                memory.set_action(task.get("intent"))

                break

            retry += 1

            print("Retry:", retry)

        if retry > MAX_RETRY:

            print("Failed task:", task)

            
