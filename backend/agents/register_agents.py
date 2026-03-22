from agents.agent_registry import registry

from agents.planner_agent import PlannerAgent
from agents.context_agent import ContextTrackingAgent
from agents.app_agent import AppDetectionAgent
from agents.api_agent import APIAgent
from agents.rag_agent import RAGAgent
from agents.workflow_agent import WorkflowAgent
from agents.ui_agent import UIAgent
from agents.browser_agent import BrowserAgent
from agents.terminal_agent import TerminalAgent
from agents.window_agent import WindowAgent
from agents.file_agent import FileAgent
from agents.skill_agent import SkillAgent
from agents.executor_agent import ExecutorAgent
from agents.memory_agent import MemoryAgent


def register_all_agents():

    registry.register(PlannerAgent())

    registry.register(ContextTrackingAgent())

    registry.register(AppDetectionAgent())

    registry.register(APIAgent())

    registry.register(RAGAgent())

    registry.register(WorkflowAgent())

    registry.register(UIAgent())

    registry.register(BrowserAgent())

    registry.register(TerminalAgent())

    registry.register(WindowAgent())

    registry.register(FileAgent())

    registry.register(SkillAgent())

    registry.register(ExecutorAgent())

    registry.register(MemoryAgent())