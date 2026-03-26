from agents.agent_registry import registry

from agents.planner_agent import PlannerAgent
from agents.context_agent import ContextTrackingAgent
from agents.app_agent import AppDetectionAgent
from agents.api_agent import APIAgent
from agents.rag_agent import RAGAgent
from agents.rag_memory_agent import RAGMemoryAgent
from agents.skill_db_agent import SkillDBAgent
from agents.message_agent import MessageAgent
from agents.skill_learning_agent import SkillLearningAgent
from agents.skill_exec_agent import SkillExecAgent
from agents.graph_planner_agent import GraphPlannerAgent
from agents.observer_agent import ObserverAgent
from agents.error_analyzer_agent import ErrorAnalyzerAgent
from agents.plugin_agent import PluginAgent
from agents.vision_reasoner_agent import VisionReasonerAgent

from agents.dev_agent import DevAgent
from agents.auto_agent import AutoAgent
from agents.code_agent import CodeAgent
from agents.text_agent import TextAgent
from agents.voice_agent import VoiceAgent
from agents.vision_agent import VisionAgent

from agents.workflow_agent import WorkflowAgent
from agents.ui_agent import UIAgent
from agents.browser_agent import BrowserAgent
from agents.terminal_agent import TerminalAgent
from agents.window_agent import WindowAgent
from agents.file_agent import FileAgent

from agents.skill_agent import SkillAgent
from agents.executor_agent import ExecutorAgent
from agents.memory_agent import MemoryAgent

from agents.self_improve_agent import SelfImproveAgent
from agents.session_agent import SessionAgent
from agents.final_core_agent import FinalCoreAgent

# ✅ STEP 76 / 77
from agents.task_understanding_agent import TaskUnderstandingAgent
from agents.advanced_planner_agent import AdvancedPlannerAgent


def register_all_agents():

    # ---------- CORE ----------

    registry.register(PlannerAgent())

    # ✅ PHASE 6
    registry.register(TaskUnderstandingAgent())
    registry.register(AdvancedPlannerAgent())

    registry.register(ContextTrackingAgent())
    registry.register(AppDetectionAgent())
    registry.register(APIAgent())
    registry.register(RAGAgent())
    registry.register(RAGMemoryAgent())
    registry.register(SkillDBAgent())
    registry.register(MessageAgent())
    registry.register(SkillLearningAgent())
    registry.register(SkillExecAgent())
    registry.register(GraphPlannerAgent())
    registry.register(ObserverAgent())
    registry.register(ErrorAnalyzerAgent())
    registry.register(PluginAgent())
    registry.register(VisionReasonerAgent())

    # ---------- HIGH PRIORITY ----------

    registry.register(DevAgent())
    registry.register(AutoAgent())
    registry.register(CodeAgent())
    registry.register(TextAgent())
    registry.register(VoiceAgent())
    registry.register(VisionAgent())

    # ---------- UI / SYSTEM ----------

    registry.register(WorkflowAgent())
    registry.register(UIAgent())
    registry.register(BrowserAgent())
    registry.register(TerminalAgent())
    registry.register(WindowAgent())
    registry.register(FileAgent())

    # ---------- LOW PRIORITY ----------

    registry.register(SkillAgent())
    registry.register(ExecutorAgent())
    registry.register(MemoryAgent())

    # ---------- PHASE 5 ----------

    registry.register(SelfImproveAgent())
    registry.register(SessionAgent())
    registry.register(FinalCoreAgent())