# agents/skill_db_agent.py

from agents.base_agent import BaseAgent

from memory.skill_db import skill_db
from memory.skill_json import load_skills, save_skills


class SkillDBAgent(BaseAgent):

    def __init__(self):
        super().__init__("SkillDBAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("skill_db"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        mode = task.get("skill_db")

        if mode == "save":

            name = task.get("name")
            data = task.get("data")

            skill_db.save_skill(name, str(data))

            skills = load_skills()
            skills[name] = data
            save_skills(skills)

            print("Skill saved:", name)

            return

        if mode == "load":

            skills = skill_db.get_skills()

            print("Skills:", skills)

            return skills