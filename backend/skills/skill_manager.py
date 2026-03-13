# skills/skill_manager.py

from skills.skills_registry import SKILLS


def execute_skill(task):

    intent = task.get("intent")

    if intent in SKILLS:

        skill = SKILLS[intent]

        skill(task)

    else:

        print("No skill found for:", intent)