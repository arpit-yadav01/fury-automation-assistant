# commands/visual_commands.py
# Handles: visual, resume, visual history, decompose
# Steps 131, 132, 133


def handle(command, cmd):
    """
    Returns True if command was handled, False otherwise.
    fury.py checks this return value to know if it should continue.
    """

    # STEP 131 — visual agent
    if cmd.startswith("visual "):
        from execution.visual_agent import run_visual_goal
        result = run_visual_goal(command[7:].strip())
        print(f"Outcome: {result['outcome']} in {result['steps']} steps")
        return True

    # STEP 132 — resume
    if cmd == "resume":
        from execution.visual_agent import resume_last_task
        from memory.task_memory import get_pending_task_summary
        summary = get_pending_task_summary()
        if summary:
            print(f"Resuming: '{summary['goal']}'")
            resume_last_task()
        else:
            print("No interrupted task.")
        return True

    # STEP 132 — visual history
    if cmd in ("visual history", "fury visual history"):
        from memory.task_memory import print_history
        print_history()
        return True

    # STEP 133 — decompose
    if cmd.startswith("decompose "):
        from execution.goal_decomposer import decompose_goal, print_plan
        plan = decompose_goal(command[10:].strip())
        print_plan(plan)
        print("Run this plan? (yes/no)")
        if input(">>> ").strip().lower() in ("yes", "y"):
            from execution.goal_decomposer import execute_plan
            execute_plan(plan)
        return True

    return False