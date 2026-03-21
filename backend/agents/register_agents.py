# agents/register_agents.py

from agents.agent_registry import registry

from agents.executor_agent import ExecutorAgent


def register_all_agents():

    registry.register(ExecutorAgent())