import json
import os

FILE = "memory/failure_log.json"


def _init():

    if not os.path.exists("memory"):
        os.makedirs("memory")

    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump([], f)


def save_failure(action, error):

    _init()

    entry = {
        "action": str(action),
        "error": str(error)
    }

    try:
        with open(FILE, "r") as f:
            data = json.load(f)

        data.append(entry)

        with open(FILE, "w") as f:
            json.dump(data, f, indent=2)

        print("⚠️ Learned from failure")

    except Exception as e:
        print("Failure memory error:", e)


def get_failures():

    _init()

    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []