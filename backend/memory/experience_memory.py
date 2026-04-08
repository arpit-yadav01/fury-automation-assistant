# import json
# import os
# from datetime import datetime

# DB_PATH = os.path.join("memory", "experience.json")


# def load_experiences():

#     if not os.path.exists(DB_PATH):
#         return []

#     try:
#         with open(DB_PATH, "r") as f:
#             return json.load(f)
#     except:
#         return []


# def save_experience(command, plan, result=True):

#     data = load_experiences()

#     data.append({
#         "command": command,
#         "plan": plan,
#         "success": result,
#         "timestamp": str(datetime.now())
#     })

#     with open(DB_PATH, "w") as f:
#         json.dump(data, f, indent=2)

#     print("Experience saved")


# # ✅ FIXED — STRICT MATCH ONLY
# def find_similar(command):

#     command = command.lower().strip()

#     data = load_experiences()

#     for exp in reversed(data):

#         cmd = exp.get("command", "").lower().strip()

#         if cmd == command:
#             return exp

#     return None

import json
import os
from datetime import datetime

# ✅ FIXED PATH
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

    # ✅ NEVER save a string plan
    if isinstance(plan, str):
        print("⚠️ Skipping save — plan is a string")
        return

    # ✅ NEVER save unknown intent
    if isinstance(plan, list):
        if all(
            isinstance(p, dict) and p.get("intent") == "unknown"
            for p in plan
        ):
            print("❌ Skipping save (unknown plan)")
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

        # ✅ SKIP bad string plans
        if isinstance(plan, str):
            continue

        # ✅ SKIP unknown plans
        if isinstance(plan, list):
            if all(
                isinstance(p, dict) and p.get("intent") == "unknown"
                for p in plan
            ):
                continue

        # ✅ ONLY return if it has a real workflow
        if isinstance(plan, dict) and "workflow" in plan:
            return exp

    return None