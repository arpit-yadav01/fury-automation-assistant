# agents/skill_learning_agent.py

from agents.base_agent import BaseAgent

from memory.skill_db import skill_db
from memory.skill_json import load_skills, save_skills


class SkillLearningAgent(BaseAgent):

    def __init__(self):
        super().__init__("SkillLearningAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("learn_skill"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        name = task.get("name")
        workflow = task.get("workflow")

        if not name or not workflow:
            return

        print("Learning skill:", name)

        skill_db.save_skill(name, str(workflow))

        skills = load_skills()
        skills[name] = workflow
        save_skills(skills)

        print("Skill stored")