import json
import os
from datetime import datetime

DB_PATH = os.path.join("memory", "experience.json")


# =========================
# LOAD
# =========================

def load_experiences():

    if not os.path.exists(DB_PATH):
        return []

    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except:
        return []


# =========================
# SAVE
# =========================

def save_experience(command, plan, result=True):

    data = load_experiences()

    data.append({
        "command": command,
        "plan": plan,
        "success": result,
        "timestamp": str(datetime.now())
    })

    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print("Experience saved")


# =========================
# FIND SIMILAR (STEP 103)
# =========================

def find_similar(command):

    command = command.lower()

    data = load_experiences()

    for exp in reversed(data):  # recent first

        cmd = exp.get("command", "").lower()

        if cmd == command:
            return exp

        # partial match
        if command in cmd or cmd in command:
            return exp

    return None