
C:\projects\fury\backend\fury.py


from execution.task_planner import create_plan
from execution.executor import execute_plan
from execution.auto_loop import run_autonomous
from execution.goal_engine import run_goal

from brain.context_memory import memory

from voice.speech_to_text import listen_once
from voice.text_to_speech import speak


# ✅ AGENT IMPORTS
from agents.register_agents import register_all_agents
from agents.agent_controller import controller
from agents.jarvis_controller import jarvis


voice_mode = False
jarvis_mode = False


# -----------------------------
# PRINT MEMORY
# -----------------------------

def show_memory():

    print("---- MEMORY ----")

    print("App:", memory.get_app())
    print("Window:", memory.get_window())
    print("Site:", memory.get_site())
    print("File:", memory.get_file())
    print("Action:", memory.get_action())

    print("----------------")


# -----------------------------
# GET COMMAND
# -----------------------------

def get_command():

    global voice_mode, jarvis_mode

    if jarvis_mode:
        text = listen_once()
        return text if text else ""

    if voice_mode:
        text = listen_once()
        return text if text else ""

    return input(">>> ").strip()


# -----------------------------
# MAIN LOOP
# -----------------------------

def start_fury():

    global voice_mode, jarvis_mode

    print("=================================")
    print("🔥 FURY AI ASSISTANT STARTED")
    print("voice mode / jarvis mode / exit")
    print("=================================")

    # ✅ REGISTER AGENTS
    register_all_agents()

    while True:

        command = get_command()

        if not command:
            continue

        cmd = command.lower()

        # -------------------------
        # EXIT
        # -------------------------

        if cmd == "exit":

            speak("Shutting down")

            print("Shutting down Fury")

            break


        # -------------------------
        # VOICE MODE
        # -------------------------

        if cmd == "voice mode":

            voice_mode = True
            jarvis_mode = False

            speak("Voice mode activated")

            continue


        if cmd == "text mode":

            voice_mode = False
            jarvis_mode = False

            speak("Text mode")

            continue


        # -------------------------
        # JARVIS MODE (UPDATED)
        # -------------------------

        if cmd == "jarvis mode":

            jarvis_mode = True
            voice_mode = False

            speak("Jarvis mode activated")

            while jarvis_mode:

                text = listen_once()

                if not text:
                    continue

                if text == "stop jarvis":
                    jarvis_mode = False
                    break

                jarvis.run_loop(text)

            continue


        if cmd == "stop jarvis":

            jarvis_mode = False

            speak("Jarvis stopped")

            continue


        # -------------------------
        # GOAL MODE (UPDATED)
        # -------------------------

        if command.startswith("goal "):

            goal = command.replace("goal ", "")

            speak("Goal mode")

            jarvis.run_loop(goal)

            continue


        # -------------------------
        # AUTO MODE
        # -------------------------

        if command.startswith("auto "):

            goal = command.replace("auto ", "")

            speak("Autonomous mode")

            run_autonomous(goal)

            continue


        # -------------------------
        # NORMAL EXECUTION
        # -------------------------

        plan = create_plan(command)

        print("\nExecution Plan:")

        if isinstance(plan, dict):
            print(plan)
        else:
            for step in plan:
                print(step)

        speak("Executing")

        controller.execute(plan)

        speak("Done")

        show_memory()


# -----------------------------

if __name__ == "__main__":
    start_fury()

    C:\projects\fury\backend\agents\agent_controller.py

    # agents/agent_controller.py

from agents.agent_registry import registry


class AgentController:

    def __init__(self):
        pass

    # -------------------------

    def execute(self, plan):

        if not plan:
            return

        # raw text → planner agent

        if isinstance(plan, str):

            agent = registry.find_agent(plan)

            if agent:

                new_plan = agent.handle(plan)

                if new_plan:
                    self.execute(new_plan)

            return

        # workflow dict

        if isinstance(plan, dict) and "workflow" in plan:

            self._execute_workflow(plan["workflow"])
            return

        # list of tasks

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

        try:

            print("Agent:", agent.name)

            agent.handle(task)

        except Exception as e:

            print("Agent error:", e)

            from agents.error_agent import ErrorRecoveryAgent

            err = ErrorRecoveryAgent()

            ok = err.handle_error(task, e)

            if not ok:
                print("Task failed:", task)

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


C:\projects\fury\backend\agents\register_agents.py

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

# ✅ NEW IMPORTS (STEP 73–75)
from agents.self_improve_agent import SelfImproveAgent
from agents.session_agent import SessionAgent
from agents.final_core_agent import FinalCoreAgent


def register_all_agents():

    registry.register(PlannerAgent())

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

    registry.register(DevAgent())

    registry.register(AutoAgent())

    registry.register(CodeAgent())

    registry.register(TextAgent())

    registry.register(VoiceAgent())

    registry.register(VisionAgent())

    registry.register(WorkflowAgent())

    registry.register(UIAgent())

    registry.register(BrowserAgent())

    registry.register(TerminalAgent())

    registry.register(WindowAgent())

    registry.register(FileAgent())

    registry.register(SkillAgent())

    registry.register(ExecutorAgent())

    registry.register(MemoryAgent())

    # ✅ STEP 73–75 ADDED

    registry.register(SelfImproveAgent())

    registry.register(SessionAgent())

    registry.register(FinalCoreAgent())


    C:\projects\fury\backend\core\final_core.py

    # core/final_core.py

from agents.agent_controller import controller

from core.self_improve import self_improve

from memory.session_db import session_db


class FinalCore:

    def __init__(self):
        pass

    # -----------------

    def execute(self, plan):

        controller.execute(plan)

        self.after_step()

    # -----------------

    def after_step(self):

        self_improve.improve()

    # -----------------

    def save_state(self):

        session_db.save("last", "ok")


final_core = FinalCore()

C:\projects\fury\backend\execution\task_planner.py

# execution/task_planner.py

from brain.command_parser import parse_command
from brain.llm_brain import interpret_with_llm
from brain.ai_interpreter import interpret_command

from brain.context_memory import memory


# -----------------------------
# helper — split command safely
# -----------------------------

def split_command(command):

    parts = command.split(" and ")

    clean = []

    for p in parts:

        p = p.strip()

        if p:
            clean.append(p)

    return clean


# -----------------------------
# CONTEXT FIX
# -----------------------------

def apply_context(task):

    intent = task.get("intent")

    win = memory.get_window()
    app = memory.get_app()
    site = memory.get_site()

    # TYPE CONTEXT

    if intent == "type_text":

        if win:
            task["window"] = win

        elif app == "browser":
            task["window"] = "chrome"

        elif app:
            task["window"] = app

    # TERMINAL CONTEXT

    if intent == "run_terminal":

        if win:
            task["window"] = win

        elif app == "browser":
            task["window"] = "chrome"

        elif app:
            task["window"] = app

    # SEARCH CONTEXT

    if intent == "web_search":

        if not task.get("site") and site:
            task["site"] = site

    return task


# -----------------------------
# helper — build workflow
# -----------------------------

def build_workflow(tasks):

    steps = []

    i = 0

    while i < len(tasks):

        t = tasks[i]

        t = apply_context(t)

        intent = t.get("intent")

        last_app = memory.get_app()
        last_site = memory.get_site()

        # -----------------------
        # OPEN APP
        # -----------------------

        if intent == "open_app":

            steps.append({
                "action": "open_app",
                "name": t.get("app")
            })


        # -----------------------
        # OPEN WEBSITE
        # -----------------------

        elif intent == "open_website":

            steps.append({
                "action": "open_url",
                "url": t.get("url")
            })


        # -----------------------
        # TYPE
        # -----------------------

        elif intent == "type_text":

            steps.append({
            "action": "type",
            "text": t.get("text")
    })

    # FIX → press enter if browser OR site exists OR website opened in same command
            if last_app == "browser" or last_site or intent == "type_text":
                steps.append({
                "action": "press",
                "key": "enter"
        })


        # -----------------------
        # CREATE FILE
        # -----------------------

        elif intent == "create_file":

            steps.append({
                "action": "create_file",
                "path": t.get("filename")
            })


        # -----------------------
        # TERMINAL
        # -----------------------

        elif intent == "run_terminal":

            steps.append({
                "action": "terminal",
                "cmd": t.get("command")
            })


        # -----------------------
        # SEARCH
        # -----------------------

        elif intent == "web_search":

            site = t.get("site", "google")
            query = t.get("query")

            if site == "youtube":

                steps.append({
                    "action": "open_url",
                    "url": "https://www.youtube.com"
                })

                steps.append({
                    "action": "wait",
                    "time": 3
                })

                steps.append({
                    "action": "type",
                    "text": query
                })

                steps.append({
                    "action": "press",
                    "key": "enter"
                })

            else:

                steps.append({
                    "action": "open_url",
                    "url": f"https://www.google.com/search?q={query}"
                })


        else:

            steps.append({
                "action": "skill",
                "intent": intent,
                "data": t
            })

        i += 1

    return {"workflow": steps}


# -----------------------------
# MAIN PLANNER
# -----------------------------

def create_plan(command):

    command = command.strip()

    ai_result = interpret_command(command)

    if ai_result:
        return [apply_context(ai_result)]

    llm_tasks = interpret_with_llm(command)

    if llm_tasks:
        return [apply_context(t) for t in llm_tasks]

    parts = split_command(command)

    tasks = []

    for part in parts:

        task = parse_command(part)

        if task:
            task = apply_context(task)
            tasks.append(task)

    if len(tasks) == 1:
        return tasks

    if len(tasks) > 1:

        print("Planner: building workflow")

        return build_workflow(tasks)

    return [{"intent": "unknown"}]

C:\projects\fury\backend\execution\executor.py

# execution/executor.py

from skills.skill_manager import execute_skill

from execution.workflow_engine import run_workflow

from brain.context_memory import memory


MAX_RETRY = 2


def execute_plan(plan):

    if not plan:
        print("No tasks to execute")
        return


    # -----------------------------
    # WORKFLOW SUPPORT
    # -----------------------------

    if isinstance(plan, dict) and "workflow" in plan:

        retry = 0

        while retry <= MAX_RETRY:

            try:

                print("Executing workflow")

                run_workflow(plan["workflow"])

                memory.set_action("workflow")

                return

            except Exception as e:

                print("Workflow error:", e)

                retry += 1

                print("Retry:", retry)

        print("Workflow failed")

        return


    # -----------------------------
    # PHASE 1 COMPATIBILITY
    # -----------------------------

    if isinstance(plan, dict):
        plan = [plan]


    for task in plan:

        if not isinstance(task, dict):
            print("Invalid task:", task)
            continue


        retry = 0

        while retry <= MAX_RETRY:

            executed = execute_skill(task)

            if executed:

                memory.set_action(task.get("intent"))

                break

            retry += 1

            print("Retry:", retry)

        if retry > MAX_RETRY:

            print("Failed task:", task)



C:\projects\fury\backend\planner\graph_planner.py
    # planner/graph_planner.py


class TaskNode:

    def __init__(self, action, data=None):

        self.action = action
        self.data = data or {}
        self.next = []


class GraphPlan:

    def __init__(self):

        self.nodes = []

    def add(self, node):

        self.nodes.append(node)

    def run(self, controller):

        for n in self.nodes:

            task = {
                "action": n.action,
                **n.data,
            }

            controller.execute(task)


def build_graph_plan(tasks):

    plan = GraphPlan()

    for t in tasks:

        node = TaskNode(
            action=t.get("action") or t.get("intent"),
            data=t,
        )

        plan.add(node)

    return plan        

C:\projects\fury\backend\agents\code_agent.py
# agents/code_agent.py

from agents.base_agent import BaseAgent

from developer.code_generator import generate_code


class CodeAgent(BaseAgent):

    def __init__(self):
        super().__init__("CodeAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("intent") == "generate_code":
            return True

        return False

    # -------------------------

    def handle(self, task):

        lang = task.get("language", "python")
        t = task.get("task", "")

        print("CodeAgent generating code")

        code = generate_code(lang, t)

        print(code)

        return code
    

    C:\projects\fury\backend\agents\skill_agent.py
    # agents/skill_agent.py

from agents.base_agent import BaseAgent

from skills.skill_manager import execute_skill


class SkillAgent(BaseAgent):

    def __init__(self):
        super().__init__("SkillAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("intent"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        intent = task.get("intent")

        if not intent:
            return

        ok = execute_skill(task)

        if not ok:
            raise Exception("Skill failed")
        

        C:\projects\fury\backend\agents\dev_agent.py

        # agents/dev_agent.py

from agents.base_agent import BaseAgent

from developer.dev_workflow import (
    open_vscode,
    create_new_file,
    write_code,
    save_file,
    run_python_file,
    run_command,
)


class DevAgent(BaseAgent):

    def __init__(self):
        super().__init__("DevAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("dev"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        cmd = task.get("dev")

        if cmd == "open_vscode":
            open_vscode()
            return

        if cmd == "new_file":
            create_new_file(task.get("name", "test.py"))
            return

        if cmd == "write":
            write_code(task.get("code", ""))
            return

        if cmd == "save":
            save_file()
            return

        if cmd == "run":
            run_python_file(task.get("name", "test.py"))
            return

        if cmd == "command":
            run_command(task.get("cmd", ""))
            return
        

        C:\projects\fury\backend\agents\auto_agent.py
        # agents/auto_agent.py

from agents.base_agent import BaseAgent

from execution.auto_mode_v2 import run_auto_v2


class AutoAgent(BaseAgent):

    def __init__(self):
        super().__init__("AutoAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("auto_v2"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        tasks = task.get("tasks")

        if not tasks:
            return

        run_auto_v2(tasks)


        C:\projects\fury\backend\core\self_improve.py
        # core/self_improve.py

from memory.memory_db import memory_db
from memory.skill_db import skill_db


class SelfImprove:

    def __init__(self):
        pass

    # -----------------

    def learn_from_history(self):

        history = memory_db.get_history()

        for h in history:

            command, action, result = h

            if not action:
                continue

            name = command

            data = {
                "action": action,
                "result": result,
            }

            skill_db.save_skill(name, str(data))

        print("SelfImprove: learned from history")

    # -----------------

    def improve(self):

        self.learn_from_history()


self_improve = SelfImprove()

C:\projects\fury\backend\memory\session_db.py
# memory/session_db.py

import sqlite3
import os


DB = "memory/session.db"


class SessionDB:

    def __init__(self):

        os.makedirs("memory", exist_ok=True)

        self.conn = sqlite3.connect(DB)

        self.create()

    # -----------------

    def create(self):

        cur = self.conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                key TEXT,
                value TEXT
            )
            """
        )

        self.conn.commit()

    # -----------------

    def save(self, key, value):

        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO sessions (key,value) VALUES (?,?)",
            (key, value),
        )

        self.conn.commit()

    # -----------------

    def load_all(self):

        cur = self.conn.cursor()

        cur.execute("SELECT key,value FROM sessions")

        return cur.fetchall()


session_db = SessionDB()