# agents/skill_exec_agent.py

from agents.base_agent import BaseAgent

from memory.skill_json import load_skills

from execution.workflow_engine import run_workflow


class SkillExecAgent(BaseAgent):

    def __init__(self):
        super().__init__("SkillExecAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("use_skill"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        name = task.get("use_skill")

        skills = load_skills()

        if name not in skills:
            print("Skill not found:", name)
            return

        workflow = skills[name]

        print("Running learned skill:", name)

        run_workflow(workflow)