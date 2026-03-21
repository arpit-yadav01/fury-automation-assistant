# agents/agent_registry.py


class AgentRegistry:

    def __init__(self):
        self.agents = []

    # -----------------------

    def register(self, agent):

        print("Register agent:", agent.name)

        self.agents.append(agent)

    # -----------------------

    def get_agents(self):
        return self.agents

    # -----------------------

    def find_agent(self, task):

        for agent in self.agents:

            try:

                if agent.can_handle(task):
                    return agent

            except Exception:
                pass

        return None


# global registry

registry = AgentRegistry()