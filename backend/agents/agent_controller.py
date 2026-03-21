# agents/agent_controller.py

from agents.agent_registry import registry


class AgentController:

    def __init__(self):
        pass

    # -------------------------

    def execute(self, plan):

        if not plan:
            return

        # raw text → planner agent

        if isinstance(plan, str):

            agent = registry.find_agent(plan)

            if agent:

                new_plan = agent.handle(plan)

                if new_plan:
                    self.execute(new_plan)

            return

        # workflow dict

        if isinstance(plan, dict) and "workflow" in plan:

            self._execute_workflow(plan["workflow"])
            return

        # list of tasks

        if isinstance(plan, dict):
            plan = [plan]

        for task in plan:

            self._execute_task(task)

    # -------------------------

    def _execute_task(self, task):

        agent = registry.find_agent(task)

        if not agent:

            print("No agent for task:", task)
            return

        print("Agent:", agent.name)

        agent.handle(task)

    # -------------------------

    def _execute_workflow(self, steps):

        for step in steps:

            agent = registry.find_agent(step)

            if not agent:

                print("No agent for step:", step)
                continue

            print("Agent:", agent.name)

            agent.handle(step)


# global controller

controller = AgentController()