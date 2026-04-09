import json
import os
from datetime import datetime

# ✅ CORRECT PATH
DB_PATH = os.path.join("memory", "experience_memory.json")


def load_experiences():

    if not os.path.exists(DB_PATH):
        return []

    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def save_experience(command, plan, result=True):

    # never save string plans
    if isinstance(plan, str):
        print("⚠️ Skipping save — plan is string")
        return

    # never save unknown intent
    if isinstance(plan, list):
        if all(isinstance(p, dict) and p.get("intent") == "unknown" for p in plan):
            print("❌ Skipping save (unknown plan)")
            return

    # never save empty workflow
    if isinstance(plan, dict) and "workflow" in plan:
        if not plan["workflow"]:
            print("⚠️ Skipping save — empty workflow")
            return

    data = load_experiences()

    data.append({
        "command": command.lower().strip(),
        "plan": plan,
        "success": result,
        "timestamp": str(datetime.now())
    })

    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print("✅ Experience saved")


def find_similar(command):

    command = command.lower().strip()
    data = load_experiences()

    for exp in reversed(data):

        cmd = exp.get("command", "").lower().strip()

        if cmd != command:
            continue

        plan = exp.get("plan")

        # skip bad plans
        if isinstance(plan, str):
            continue

        if isinstance(plan, list):
            if all(isinstance(p, dict) and p.get("intent") == "unknown" for p in plan):
                continue

        # only return real workflows
        if isinstance(plan, dict) and "workflow" in plan:
            if plan["workflow"]:
                return exp

    return None