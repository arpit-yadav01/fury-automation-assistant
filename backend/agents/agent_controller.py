# agents/agent_controller.py

from agents.agent_registry import registry


class AgentController:

    def __init__(self):
        pass

    # -------------------------

    def execute(self, plan):

        if not plan:
            return

        current = plan

        # allow multi-agent pipeline (Phase-6)

        for _ in range(10):

            # -------------------------
            # workflow
            # -------------------------

            if isinstance(current, dict) and "workflow" in current:

                self._execute_workflow(current["workflow"])
                return

            # -------------------------
            # single task dict
            # -------------------------

            if isinstance(current, dict):

                agent = registry.find_agent(current)

                if not agent:
                    print("No agent for task:", current)
                    return

                try:

                    print("Agent:", agent.name)

                    result = agent.handle(current)

                    # if agent returns new task → continue chain

                    if isinstance(result, dict):
                        current = result
                        continue

                    # if nothing returned → stop
                    return

                except Exception as e:

                    print("Agent error:", e)

                    from agents.error_agent import ErrorRecoveryAgent

                    err = ErrorRecoveryAgent()

                    ok = err.handle_error(current, e)

                    if not ok:
                        print("Task failed:", current)

                    return

            # -------------------------
            # list
            # -------------------------

            if isinstance(current, list):

                for task in current:
                    self.execute(task)

                return

            # -------------------------
            # string
            # -------------------------

            if isinstance(current, str):

                agent = registry.find_agent(current)

                if agent:

                    result = agent.handle(current)

                    if result:
                        current = result
                        continue

                return

        print("Controller loop limit reached")

    # -------------------------

    def _execute_workflow(self, steps):

        for step in steps:

            agent = registry.find_agent(step)

            if not agent:

                print("No agent for step:", step)
                continue

            try:

                print("Agent:", agent.name)

                agent.handle(step)

            except Exception as e:

                print("Agent error:", e)

                from agents.error_agent import ErrorRecoveryAgent

                err = ErrorRecoveryAgent()

                ok = err.handle_error(step, e)

                if not ok:
                    print("Step failed:", step)


# global controller

controller = AgentController()