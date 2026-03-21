from agents.agent_registry import registry

from agents.executor_agent import ExecutorAgent
from agents.planner_agent import PlannerAgent
from agents.memory_agent import MemoryAgent
from agents.workflow_agent import WorkflowAgent
from agents.ui_agent import UIAgent


def register_all_agents():

    registry.register(PlannerAgent())

    registry.register(WorkflowAgent())

    registry.register(UIAgent())

    registry.register(ExecutorAgent())

    registry.register(MemoryAgent())