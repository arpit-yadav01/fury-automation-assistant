import json
import os
from datetime import datetime

DB_PATH = os.path.join("memory", "experience_memory.json")


def load_memory():

    if not os.path.exists(DB_PATH):
        return []

    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def save_memory(data):

    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)


# ---------------------

def save_experience(command, plan, result=True):

    memory = load_memory()

    entry = {
        "command": command,
        "plan": plan,
        "success": result,
        "timestamp": datetime.now().isoformat()
    }

    memory.append(entry)

    # keep memory size safe
    if len(memory) > 100:
        memory = memory[-100:]

    save_memory(memory)

    print("Experience saved")


# ---------------------

def find_similar(command):

    memory = load_memory()

    for item in reversed(memory):

        if item["command"] == command and item["success"]:
            return item

    return None