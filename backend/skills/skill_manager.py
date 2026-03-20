from skills.skills_registry import SKILLS
from brain.context_memory import memory


def execute_skill(task):

    intent = task.get("intent")

    if not intent:
        return False

    skill = SKILLS.get(intent)

    if not skill:
        return False

    try:

        skill(task)

        memory.set_action(intent)

        return True

    except Exception as e:

        print("Skill error:", e)

        return False