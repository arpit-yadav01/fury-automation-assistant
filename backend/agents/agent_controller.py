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

        for _ in range(15):  # slightly increased safety

            # -------------------------
            # WORKFLOW
            # -------------------------

            if isinstance(current, dict) and "workflow" in current:

                self._execute_workflow(current["workflow"])
                return

            # -------------------------
            # SINGLE TASK
            # -------------------------

            if isinstance(current, dict):

                agent = registry.find_agent(current)

                if not agent:
                    print("No agent for task:", current)
                    return

                try:

                    print("Agent:", agent.name)

                    result = agent.handle(current)

                    # 🔥 CONTINUE CHAIN
                    if isinstance(result, dict):
                        current = result
                        continue

                    # ✅ allow True (operator success)
                    if result is True:
                        return

                    # stop if nothing
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
            # LIST
            # -------------------------

            if isinstance(current, list):

                for task in current:
                    self.execute(task)

                return

            # -------------------------
            # RAW STRING (ENTRY POINT)
            # -------------------------

            if isinstance(current, str):

                agent = registry.find_agent(current)

                if agent:

                    print("Agent:", agent.name)

                    result = agent.handle(current)

                    if isinstance(result, dict):
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

                result = agent.handle(step)

                # 🔥 allow chained workflow steps
                if isinstance(result, dict):
                    self.execute(result)

            except Exception as e:

                print("Agent error:", e)

                from agents.error_agent import ErrorRecoveryAgent

                err = ErrorRecoveryAgent()

                ok = err.handle_error(step, e)

                if not ok:
                    print("Step failed:", step)


# global controller

controller = AgentController()