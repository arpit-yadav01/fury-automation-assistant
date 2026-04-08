

from dotenv import load_dotenv
load_dotenv()

from execution.auto_loop import run_autonomous
from brain.context_memory import memory

from voice.speech_to_text import listen_once
from voice.text_to_speech import speak

# AGENTS
from agents.register_agents import register_all_agents
from agents.agent_controller import controller
from agents.jarvis_controller import jarvis

# ✅ STEP 102 FIX
from core.final_core import final_core


voice_mode = False
jarvis_mode = False


# -------------------------
# MEMORY DISPLAY
# -------------------------

def show_memory():

    print("---- MEMORY ----")

    print("App:", memory.get_app())
    print("Window:", memory.get_window())
    print("Site:", memory.get_site())
    print("File:", memory.get_file())
    print("Action:", memory.get_action())

    print("----------------")


# -------------------------
# INPUT HANDLER
# -------------------------

def get_command():

    global voice_mode, jarvis_mode

    if jarvis_mode:
        text = listen_once()
        return text if text else ""

    if voice_mode:
        text = listen_once()
        return text if text else ""

    return input(">>> ").strip()


# -------------------------
# MAIN LOOP
# -------------------------

def start_fury():

    global voice_mode, jarvis_mode

    print("=================================")
    print("🔥 FURY AI ASSISTANT STARTED")
    print("voice mode / jarvis mode / exit")
    print("=================================")

    # 🔥 REGISTER ALL AGENTS
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
        # MODES
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

        # -------------------------
        # GOAL MODE
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

        # =========================
        # ✅ FINAL PIPELINE (FIXED)
        # =========================

        print("\nSending to Agent System...")

        speak("Executing")

        # ✅ USE FINAL CORE (VERY IMPORTANT)
        final_core.execute(command)

        speak("Done")

        show_memory()


# -------------------------
# ENTRY POINT
# -------------------------

if __name__ == "__main__":
    start_fury()

from agents.agent_registry import registry


class AgentController:

    def __init__(self):
        pass

    # -------------------------

    def execute(self, plan):

        if not plan:
            return

        # =========================
        # LIST HANDLING
        # =========================

        if isinstance(plan, list):

            for step in plan:
                self.execute(step)

            return

        current = plan

        # =========================
        # MAIN LOOP
        # =========================

        for _ in range(10):

            # -------------------------
            # WORKFLOW DIRECT EXECUTION
            # -------------------------

            if isinstance(current, dict) and "workflow" in current:
                self._execute_workflow(current["workflow"])
                return

            # -------------------------
            # DICT TASK
            # -------------------------

            if isinstance(current, dict):

                agent = registry.find_agent(current)

                if not agent:
                    print("No agent for task:", current)
                    return

                try:

                    print("Agent:", agent.name)

                    result = agent.handle(current)

                    # =========================
                    # 🔥 CRITICAL FIX — PLANNER HANDOFF
                    # =========================

                    from execution.task_planner import create_plan

                    # parse_command → planner
                    if isinstance(result, dict) and result.get("intent") == "parse_command":
                        result = create_plan(result.get("text"))

                    # string fallback → planner
                    if isinstance(result, str):
                        result = create_plan(result)

                    # continue chain
                    if isinstance(result, dict) or isinstance(result, list):

    # 🔥 PREVENT SAME LOOP
                        if result == current:
                            return  

                        current = result
                        continue

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
            # STRING INPUT
            # -------------------------

            if isinstance(current, str):

                agent = registry.find_agent(current)

                if not agent:
                    print("No agent for input:", current)
                    return

                try:

                    print("Agent:", agent.name)

                    result = agent.handle(current)

                    # 🔥 SAME FIX FOR STRING FLOW
                    from execution.task_planner import create_plan

                    if isinstance(result, dict) and result.get("intent") == "parse_command":
                        result = create_plan(result.get("text"))

                    if isinstance(result, str):
                        result = create_plan(result)

                    if isinstance(result, dict) or isinstance(result, list):
                        current = result
                        continue

                    return

                except Exception as e:

                    print("Agent error:", e)
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

                if isinstance(result, dict) or isinstance(result, list):
                    self.execute(result)

            except Exception as e:

                print("Agent error:", e)


# -------------------------
# GLOBAL
# -------------------------

controller = AgentController()



from brain.command_parser import parse_command
from brain.llm_brain import interpret_with_llm
from brain.ai_interpreter import interpret_command

from brain.context_memory import memory
from memory.experience_memory import find_similar
from skills.auto_skill_builder import find_best_skill

print("🔥 FINAL TASK PLANNER (PHASE-8 FIXED)")


# -------------------------
# SPLIT COMMAND
# -------------------------

def split_command(command):

    command = command.replace(",", " and ")
    command = command.replace(" then ", " and ")

    return [p.strip() for p in command.split(" and ") if p.strip()]


# -------------------------
# APPLY CONTEXT
# -------------------------

def apply_context(task):

    if task.get("intent") == "web_search":

        site = memory.get_site()

        if site:
            task["site"] = site

    return task


# =========================
# BUILD WORKFLOW
# =========================

def build_workflow(tasks):

    steps = []
    current_site = None

    for t in tasks:

        t = apply_context(t)
        intent = t.get("intent")

        if intent == "open_website":

            url = t.get("url")

            steps.append({"action": "open_url", "url": url})

            if "youtube" in url:
                current_site = "youtube"
            elif "google" in url:
                current_site = "google"

        elif intent == "web_search":

            query = t.get("query")
            site = t.get("site") or current_site or "google"

            if site == "youtube":

                steps.append({"action": "wait", "time": 2})
                steps.append({"action": "press", "key": "/"})
                steps.append({"action": "wait", "time": 1})
                steps.append({"action": "type", "text": query})
                steps.append({"action": "press", "key": "enter"})

            else:

                steps.append({
                    "action": "open_url",
                    "url": "https://www.google.com"
                })

                steps.append({"action": "wait", "time": 2})
                steps.append({"action": "type", "text": query})
                steps.append({"action": "press", "key": "enter"})

        elif intent == "type_text":

            steps.append({
                "action": "type",
                "text": t.get("text")
            })

        else:

            steps.append({
                "action": "skill",
                "data": t
            })

    return {"workflow": steps}


# =========================
# SINGLE TASK HANDLER
# =========================

def handle_single_task(task):

    intent = task.get("intent")

    if intent == "web_search":
        return build_workflow([task])

    raw = task.get("raw", "").lower()

    if "youtube" in raw and "search" in raw:

        query = raw.replace("open youtube", "").replace("search", "").strip()

        return build_workflow([
            {"intent": "open_website", "url": "https://www.youtube.com"},
            {"intent": "web_search", "query": query, "site": "youtube"}
        ])

    if intent == "open_app":
        return {"workflow": [{"action": "skill", "data": task}]}

    return [task]


# =========================
# MAIN PLANNER
# =========================

def create_plan(command):

    # =========================
    # STEP 105 — SMART SKILL
    # =========================

    skill_name, plan = find_best_skill(command)

    if plan and len(command.split()) <= 4:

        print(f"⚡ Smart skill used: {skill_name}")

        if isinstance(plan, dict) and "workflow" in plan:
            return plan

        if isinstance(plan, list):
            return {"workflow": plan}

    # =========================
    # STEP 103 — MEMORY (FIXED)
    # =========================

    exp = find_similar(command)

    if exp and exp.get("success"):

        print("⚡ Using past experience")

        plan = exp.get("plan")

        # 🔥 NORMALIZE PLAN
        if isinstance(plan, dict) and "workflow" in plan:
            return plan

        if isinstance(plan, list):
            return {"workflow": plan}

        if isinstance(plan, dict):
            return {"workflow": [plan]}

        return [{"intent": "unknown"}]

    # =========================
    # NORMAL FLOW
    # =========================

    parts = split_command(command)

    tasks = []

    for part in parts:
        task = parse_command(part)
        if task:
            tasks.append(task)

    if len(tasks) > 1:
        print("Planner: building workflow")
        return build_workflow(tasks)

    if tasks:
        return handle_single_task(tasks[0])

    ai_result = interpret_command(command)

    if ai_result:
        return handle_single_task(ai_result)

    llm_tasks = interpret_with_llm(command)

    if llm_tasks:
        return build_workflow(llm_tasks)

    return [{"intent": "unknown"}]



from memory.experience_memory import load_experiences

AUTO_SKILLS = {}
THRESHOLD = 3


def normalize(command):
    return command.lower().strip()


def build_auto_skills():

    AUTO_SKILLS.clear()

    data = load_experiences()

    counter = {}

    for exp in data:

        cmd = normalize(exp.get("command", ""))

        if cmd not in counter:
            counter[cmd] = []

        counter[cmd].append(exp)

    for cmd, logs in counter.items():

        if len(logs) >= THRESHOLD:

            skill_name = generate_skill_name(cmd)

            AUTO_SKILLS[skill_name] = {
                "plan": logs[-1].get("plan"),
                "command": cmd
            }

    return AUTO_SKILLS


# ✅ FIXED — STRICT MATCH
def find_best_skill(user_command):

    user_command = normalize(user_command)

    skills = build_auto_skills()

    for name, data in skills.items():

        cmd = data.get("command")
        plan = data.get("plan")

        if not cmd or not plan:
            continue

        # ✅ ONLY EXACT MATCH
        if user_command == cmd:
            return name, plan

    return None, None


def generate_skill_name(command):

    if "youtube" in command and "lofi" in command:
        return "play_lofi"

    if "youtube" in command and "music" in command:
        return "play_music"

    if "google" in command:
        return "search_google"

    return command.replace(" ", "_")[:30]


# agents/workflow_agent.py

from agents.base_agent import BaseAgent

from execution.workflow_engine import run_workflow


class WorkflowAgent(BaseAgent):

    def __init__(self):
        super().__init__("WorkflowAgent")

    # -------------------------

    def can_handle(self, task):

        if isinstance(task, dict) and "workflow" in task:
            return True

        if isinstance(task, dict) and task.get("action"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        if "workflow" in task:

            print("WorkflowAgent → run_workflow")

            run_workflow(task["workflow"])

            return

        if task.get("action"):

            print("WorkflowAgent → step")

            run_workflow([task])

            return
        

from agents.base_agent import BaseAgent

from execution.executor import execute_plan
from execution.workflow_engine import run_workflow
from skills.skill_manager import execute_skill
from skills.skills_registry import SKILLS


class ExecutorAgent(BaseAgent):

    def __init__(self):
        super().__init__("ExecutorAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        # workflow
        if "workflow" in task:
            return True

        # step
        if task.get("action"):
            return True

        # ✅ ONLY HANDLE VALID SKILLS
        if task.get("intent") in SKILLS:
            return True

        return False

    # -------------------------

    def handle(self, task):

        # -------------------------
        # WORKFLOW
        # -------------------------

        if "workflow" in task:

            print("ExecutorAgent → workflow")

            run_workflow(task["workflow"])

            return

        # -------------------------
        # SINGLE STEP
        # -------------------------

        if task.get("action"):

            print("ExecutorAgent → step")

            run_workflow([task])

            return

        # -------------------------
        # SKILL EXECUTION
        # -------------------------

        intent = task.get("intent")

        if intent in SKILLS:

            print("ExecutorAgent → skill:", intent)

            success = execute_skill(intent, task)

            if isinstance(success, dict):
                return success

            return

        # -------------------------
        # FALLBACK
        # -------------------------

        print("ExecutorAgent → fallback")

        execute_plan(task)




# skills/skills_registry.py

from browser.browser_agent import open_website, smart_search
from automation.file_manager import create_file, write_to_file
from developer.terminal_engine import run_terminal_command
from vision.ui_click import click_text
from automation.typing_engine import type_text, smart_type
from automation.software_control import open_application
from brain.context_memory import memory

from skills.auto_skill_builder import build_auto_skills

from developer.dev_workflow import (
    open_vscode,
    create_new_file,
    write_code,
    save_file,
    run_python_file,
    run_command,
)


# -------------------------
# OPEN APP
# -------------------------

def skill_open_app(task):

    app = task.get("app")

    if not app:
        return

    open_application(app)

    memory.set_app(app)

    if app == "vscode":
        memory.set_window("code")
    elif app == "notepad":
        memory.set_window("notepad")
    else:
        memory.set_window(app)

    memory.set_action("open_app")


# -------------------------
# OPEN WEBSITE
# -------------------------

def skill_open_website(task):

    url = task.get("url")

    if not url:
        return

    open_website(url)

    memory.set_site(url)
    memory.set_app("browser")
    memory.set_window("chrome")
    memory.set_action("open_website")


# -------------------------
# WEB SEARCH
# -------------------------

def skill_web_search(task):

    query = task.get("query")

    if not query:
        open_website("https://google.com")
        return

    smart_search(query)

    memory.set_action("web_search")


# -------------------------
# CREATE FILE
# -------------------------

def skill_create_file(task):

    filename = task.get("filename")

    if filename:
        create_file(filename)
        memory.set_file(filename)
        memory.set_action("create_file")


# -------------------------
# WRITE FILE
# -------------------------

def skill_write_file(task):

    filename = task.get("filename")
    text = task.get("text")

    if filename and text:
        write_to_file(filename, text)


# -------------------------
# TYPE TEXT
# -------------------------

def skill_type_text(task):

    text = task.get("text")
    window = task.get("window")

    if not text:
        return

    if window:
        smart_type(text, window)
    else:
        type_text(text)

    memory.set_action("type_text")


# -------------------------
# TERMINAL
# -------------------------

def skill_run_terminal(task):

    command = task.get("command")

    if command:
        run_terminal_command(command)
        memory.set_action("run_terminal")


# -------------------------
# CLICK
# -------------------------

def skill_click_text(task):

    text = task.get("text")

    if text:
        click_text(text)


# -------------------------
# DEV SKILLS
# -------------------------

def skill_open_vscode(task):
    open_vscode()


def skill_create_code_file(task):

    filename = task.get("filename", "test.py")
    create_new_file(filename)


def skill_write_code(task):

    code = task.get("code")

    if code:
        write_code(code)


def skill_save_file(task):
    save_file()


def skill_run_python(task):

    filename = task.get("filename", "test.py")
    run_python_file(filename)


def skill_dev_command(task):

    cmd = task.get("command")

    if cmd:
        run_command(cmd)


# =========================
# 🔥 EXECUTE SKILL (FIXED)
# =========================

def execute_skill(intent, task):

    # -------------------------
    # AUTO SKILLS
    # -------------------------

    auto = build_auto_skills()

    if intent in auto:

        print("⚡ Using learned skill:", intent)

        return {
            "workflow": auto[intent]
}

    # -------------------------
    # NORMAL SKILLS
    # -------------------------

    skill = SKILLS.get(intent)

    if skill:
        return skill(task)

    print("Skill not found:", intent)


# -------------------------
# MAP
# -------------------------

SKILLS = {

    "open_app": skill_open_app,
    "open_website": skill_open_website,
    "web_search": skill_web_search,
    "create_file": skill_create_file,
    "write_file": skill_write_file,
    "type_text": skill_type_text,
    "run_terminal": skill_run_terminal,
    "click_text": skill_click_text,

    "open_vscode": skill_open_vscode,
    "create_code_file": skill_create_code_file,
    "write_code": skill_write_code,
    "save_file": skill_save_file,
    "run_python": skill_run_python,
    "run_dev_command": skill_dev_command,
}


# core/final_core.py

from agents.agent_controller import controller
from core.self_improve import self_improve
from memory.session_db import session_db

# ✅ STEP 102
from memory.experience_memory import save_experience
from brain.pattern_engine import get_frequent_command

class FinalCore:

    def __init__(self):
        pass

    # -----------------

    def execute(self, plan):

        # -----------------
        # EXECUTE PLAN
        # -----------------

        controller.execute(plan)

        # -----------------
        # SAVE EXPERIENCE (SAFE)
        # -----------------

        try:
            command = None

            if isinstance(plan, dict):
                command = plan.get("raw") or plan.get("command") or str(plan)
            else:
                command = str(plan)

            save_experience(command, plan, result=True)

        except Exception as e:
            print("Experience save failed:", e)

        # -----------------

        self.after_step()

    # -----------------

    def after_step(self):

        self_improve.improve()

    # -----------------

    def save_state(self):

        session_db.save("last", "ok")


    

patterns = get_frequent_command()

if patterns:
    print("📊 Frequent actions:", patterns[:2])

# global instance
final_core = FinalCore()


