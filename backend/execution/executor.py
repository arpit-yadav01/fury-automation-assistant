# execution/executor.py

from skills.skill_manager import execute_skill

# STEP 24
from execution.workflow_engine import run_workflow


def execute_plan(plan):

    if not plan:
        print("No tasks to execute")
        return


    # -----------------------------
    # STEP 24 — WORKFLOW SUPPORT
    # -----------------------------

    if isinstance(plan, dict) and "workflow" in plan:

        print("Executing workflow")

        run_workflow(plan["workflow"])

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


        executed = execute_skill(task)


        if not executed:
            print("Unknown task:", task)