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

# =========================
# PHASE 6
# =========================

from agents.task_understanding_agent import TaskUnderstandingAgent
from agents.goal_solver_agent import GoalSolverAgent
from agents.strategy_agent import StrategyAgent
from agents.advanced_planner_agent import AdvancedPlannerAgent
from agents.subtask_agent import SubtaskAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.code_reasoner_agent import CodeReasonerAgent
from agents.error_fix_agent import ErrorFixAgent
from agents.ui_layout_agent import UILayoutAgent

# STEP 84 + 85
from agents.context_engine_agent import ContextEngineAgent
from agents.decision_agent import DecisionAgent

# STEP 87
from agents.experience_agent import ExperienceAgent

# STEP 88 / 89 / 90
from agents.reflection_agent import ReflectionAgent
from agents.retry_agent import RetryAgent
from agents.thinking_agent import ThinkingAgent

# PHASE 7
from agents.app_intelligence_agent import AppIntelligenceAgent
from agents.ui_action_agent import UIActionAgent
from agents.vision_target_agent import VisionTargetAgent
from agents.ui_planner_agent import UIPlannerAgent
from agents.target_selection_agent import TargetSelectionAgent
from agents.operator_agent import OperatorAgent
from agents.multi_app_agent import MultiAppAgent
from agents.screen_memory_agent import ScreenMemoryAgent
from agents.navigation_agent import NavigationAgent

def register_all_agents():

    # =========================
    # THINKING LAYER (STEP 90)
    # =========================

    registry.register(ThinkingAgent())   # MUST BE FIRST

    # ---------- CORE ----------

    registry.register(PlannerAgent())

    # ---------- PHASE 6 PIPELINE ----------

    registry.register(TaskUnderstandingAgent())
    registry.register(GoalSolverAgent())
    registry.register(StrategyAgent())
    registry.register(AdvancedPlannerAgent())
    registry.register(SubtaskAgent())

    registry.register(ContextEngineAgent())
    registry.register(DecisionAgent())

    # =========================
    # 🔥 PHASE 7 CRITICAL (BEFORE EXECUTION)
    # =========================

    registry.register(MultiAppAgent())        # ✅ Step 96
    registry.register(ScreenMemoryAgent())   # ✅ Step 97
    registry.register(NavigationAgent())   

    # =========================
    # EXECUTION LAYER
    # =========================

    registry.register(WorkflowAgent())
    registry.register(ExecutorAgent())   # ⚠️ MUST COME AFTER ABOVE

    # ---------- SYSTEM ----------

    registry.register(ContextTrackingAgent())
    registry.register(AppDetectionAgent())
    registry.register(AppIntelligenceAgent())

    registry.register(APIAgent())
    registry.register(RAGAgent())
    registry.register(RAGMemoryAgent())
    registry.register(SkillDBAgent())
    registry.register(MessageAgent())
    registry.register(SkillLearningAgent())
    registry.register(SkillExecAgent())
    registry.register(GraphPlannerAgent())
    registry.register(ObserverAgent())

    # ---------- ERROR ----------

    registry.register(ErrorAnalyzerAgent())
    registry.register(ErrorFixAgent())
    registry.register(RetryAgent())

    registry.register(PluginAgent())
    registry.register(VisionReasonerAgent())

    # ---------- HIGH ----------

    registry.register(DevAgent())
    registry.register(AutoAgent())
    registry.register(CodeAgent())
    registry.register(CodeReasonerAgent())
    registry.register(TextAgent())
    registry.register(VoiceAgent())
    registry.register(VisionAgent())

    registry.register(VisionTargetAgent())
    registry.register(UILayoutAgent())
    registry.register(TargetSelectionAgent())

    # ---------- UI ----------

    registry.register(UIAgent())
    registry.register(UIPlannerAgent())
    registry.register(UIActionAgent())
    registry.register(OperatorAgent())

    registry.register(BrowserAgent())
    registry.register(TerminalAgent())
    registry.register(WindowAgent())
    registry.register(FileAgent())

    # ---------- LOW / LEARNING ----------

    registry.register(SkillAgent())
    registry.register(MemoryAgent())
    registry.register(KnowledgeAgent())
    registry.register(ExperienceAgent())
    registry.register(ReflectionAgent())

    # ---------- CORE FINAL ----------

    registry.register(SelfImproveAgent())
    registry.register(SessionAgent())
    registry.register(FinalCoreAgent())