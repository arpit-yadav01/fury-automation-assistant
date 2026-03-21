# agents/agent_controller.py

from agents.agent_registry import registry


class AgentController:

    def __init__(self):
        pass

    # -------------------------

    def execute(self, plan):

        if not plan:
            print("No plan")
            return

        if isinstance(plan, dict) and "workflow" in plan:

            self._execute_workflow(plan["workflow"])
            return

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