# agents/base_agent.py


class BaseAgent:

    def __init__(self, name):
        self.name = name

    def can_handle(self, task):
        """
        Return True if this agent can handle task
        """
        return False

    def handle(self, task):
        """
        Execute task
        """
        raise NotImplementedError