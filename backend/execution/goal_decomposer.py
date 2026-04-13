# execution/goal_decomposer.py
# STEP 133 — Goal decomposer
#
# Takes a complex goal and breaks it into ordered sub-tasks.
# Each sub-task is either:
#   - a visual task (runs through visual_agent)
#   - a command task (runs through final_core / existing pipeline)
#
# Examples:
#   "apply to this job" →
#     1. visual: open linkedin
#     2. visual: find the job posting
#     3. visual: click apply
#     4. visual: fill in name, email
#     5. visual: submit application
#
#   "solve leetcode problem two sum" →
#     1. visual: open leetcode.com
#     2. visual: find problem two sum
#     3. visual: read the problem
#     4. visual: write solution in python
#     5. visual: run and submit

import os
import json
import re
from openai import OpenAI

GROQ_KEY = os.getenv("GROQ_API_KEY")
client = None
if GROQ_KEY:
    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

# -------------------------
# SYSTEM PROMPT
# -------------------------

DECOMPOSE_PROMPT = """You are Fury's goal decomposer for a Windows PC agent.
Break the given goal into ordered sub-tasks that can be executed step by step.

Return ONLY a JSON object. No explanation. No markdown. No backticks.

Format:
{
  "goal": "<original goal>",
  "complexity": "simple" | "medium" | "complex",
  "estimated_steps": <number>,
  "subtasks": [
    {
      "id": 1,
      "type": "visual",
      "description": "<what to do>",
      "goal": "<exact visual agent goal string>",
      "depends_on": [],
      "optional": false
    }
  ]
}

Task types:
- "visual": requires seeing the screen (use for: clicking, filling forms, navigating websites)
- "command": use existing Fury command pipeline (use for: opening apps, creating files, searching)

Rules:
- Break into smallest possible atomic steps
- Each step should be achievable in 1-5 visual agent iterations
- depends_on lists IDs of tasks that must complete first
- optional=true for steps that can be skipped if needed
- Keep goal strings clear and specific for visual agent
- For web tasks, include the website URL in the goal
"""

# -------------------------
# MAIN FUNCTION
# -------------------------

def decompose_goal(goal, context=None):
    """
    Break a complex goal into ordered sub-tasks.

    Returns a plan dict with subtasks list.
    Falls back to single visual task if LLM unavailable.
    """
    if not goal:
        return _single_task(goal)

    if client is None:
        print("Decomposer: no LLM client, using single task")
        return _single_task(goal)

    try:
        user_content = f"Goal: {goal}"
        if context:
            user_content += f"\nContext: {json.dumps(context)}"

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": DECOMPOSE_PROMPT},
                {"role": "user", "content": user_content}
            ],
            temperature=0.2,
            max_tokens=800
        )

        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"```json|```", "", raw)
        plan = json.loads(raw)

        _print_decomposition(plan)
        return plan

    except Exception as e:
        print(f"Decomposer error: {e}")
        return _single_task(goal)


# -------------------------
# EXECUTE PLAN
# -------------------------

def execute_plan(plan, stop_on_failure=False):
    """
    Execute a decomposed plan step by step.

    Args:
        plan: the plan dict from decompose_goal()
        stop_on_failure: if True, stop when a subtask fails

    Returns:
        dict with results for each subtask
    """
    from execution.visual_agent import run_visual_goal
    from core.final_core import final_core

    subtasks = plan.get("subtasks", [])
    results = {}
    completed = set()

    print(f"\n🚀 Executing plan: {plan.get('goal')}")
    print(f"   {len(subtasks)} subtasks\n")

    for task in subtasks:
        task_id = task.get("id")
        task_type = task.get("type", "visual")
        description = task.get("description", "")
        goal_str = task.get("goal", description)
        depends_on = task.get("depends_on", [])
        optional = task.get("optional", False)

        # check dependencies
        for dep in depends_on:
            if dep not in completed:
                dep_result = results.get(dep, {})
                if dep_result.get("outcome") not in ("success", "skipped"):
                    print(f"⏭️  Skipping task {task_id} — dependency {dep} not completed")
                    results[task_id] = {"outcome": "skipped", "reason": f"dependency {dep} failed"}
                    if optional:
                        completed.add(task_id)
                    continue

        print(f"\n--- Subtask {task_id}: {description} ---")

        if task_type == "visual":
            result = run_visual_goal(goal_str)
            results[task_id] = result
            outcome = result.get("outcome")

        elif task_type == "command":
            try:
                final_core.execute(goal_str)
                results[task_id] = {"outcome": "success"}
                outcome = "success"
            except Exception as e:
                results[task_id] = {"outcome": "failed", "reason": str(e)}
                outcome = "failed"

        else:
            results[task_id] = {"outcome": "skipped", "reason": "unknown type"}
            outcome = "skipped"

        if outcome == "success":
            completed.add(task_id)
            print(f"✅ Subtask {task_id} done")
        elif optional:
            completed.add(task_id)
            print(f"⚠️  Subtask {task_id} failed (optional, continuing)")
        else:
            print(f"❌ Subtask {task_id} failed")
            if stop_on_failure:
                print("Stopping plan execution.")
                break

    # summary
    total = len(subtasks)
    success_count = sum(1 for r in results.values() if r.get("outcome") == "success")
    print(f"\n{'='*40}")
    print(f"Plan complete: {success_count}/{total} subtasks succeeded")
    print(f"{'='*40}\n")

    return results


# -------------------------
# PRINT PLAN
# -------------------------

def print_plan(plan):
    """Print a human-readable plan."""
    print(f"\n{'='*50}")
    print(f"🧩 Plan: {plan.get('goal')}")
    print(f"   Complexity : {plan.get('complexity', '?')}")
    print(f"   Est. steps : {plan.get('estimated_steps', '?')}")
    print(f"{'='*50}")

    for task in plan.get("subtasks", []):
        icon = "👁️" if task.get("type") == "visual" else "⚡"
        optional = " (optional)" if task.get("optional") else ""
        deps = f" [needs: {task['depends_on']}]" if task.get("depends_on") else ""
        print(f"  {icon} [{task['id']}] {task['description']}{optional}{deps}")

    print()


# -------------------------
# HELPERS
# -------------------------

def _single_task(goal):
    """Fallback — wrap goal as single visual task."""
    return {
        "goal": goal,
        "complexity": "simple",
        "estimated_steps": 5,
        "subtasks": [
            {
                "id": 1,
                "type": "visual",
                "description": goal,
                "goal": goal,
                "depends_on": [],
                "optional": False
            }
        ]
    }


def _print_decomposition(plan):
    print(f"\n🧩 Decomposed into {len(plan.get('subtasks', []))} subtasks")
    print(f"   Complexity: {plan.get('complexity', '?')}")