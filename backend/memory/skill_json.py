# memory/skill_json.py

import json
import os


FILE = "memory/skills.json"


def load_skills():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)


def save_skills(data):

    os.makedirs("memory", exist_ok=True)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)