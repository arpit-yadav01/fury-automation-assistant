# memory/json_memory.py

import json
import os


FILE = "memory/memory.json"


def load_memory():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)


def save_memory(data):

    os.makedirs("memory", exist_ok=True)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)