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

            
# agents/error_analyzer_agent.py

from agents.base_agent import BaseAgent

from core.message_bus import bus


class ErrorAnalyzerAgent(BaseAgent):

    def __init__(self):
        super().__init__("ErrorAnalyzerAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("error"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        print("ErrorAnalyzerAgent")

        error = task.get("error")
        last = task.get("last_task")

        print("Error:", error)

        decision = {
            "retry": False,
            "skip": False,
            "replan": False,
        }

        # simple logic

        if "not found" in str(error).lower():
            decision["retry"] = True

        elif "timeout" in str(error).lower():
            decision["retry"] = True

        else:
            decision["replan"] = True

        bus.send(
            "ErrorAnalyzer",
            "controller",
            decision,
        )

        return decision
    
    # agents/observer_agent.py

from agents.base_agent import BaseAgent

from automation.window_manager import get_active_window_title
from vision.text_detection import find_text_on_screen

from brain.context_memory import memory


class ObserverAgent(BaseAgent):

    def __init__(self):
        super().__init__("ObserverAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("observe"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        print("ObserverAgent")

        window = get_active_window_title()

        last_action = memory.get_action()

        result = {
            "window": window,
            "action": last_action,
        }

        text = task.get("check_text")

        if text:

            pos = find_text_on_screen(text)

            result["text_found"] = pos is not None

        print("OBS:", result)

        return result
    
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



from dotenv import load_dotenv
load_dotenv()
from execution.task_planner import create_plan
from execution.auto_loop import run_autonomous

from brain.context_memory import memory

from voice.speech_to_text import listen_once
from voice.text_to_speech import speak

# AGENTS
from agents.register_agents import register_all_agents
from agents.agent_controller import controller
from agents.jarvis_controller import jarvis

# FIX-1 FinalCore
from core.final_core import final_core


voice_mode = False
jarvis_mode = False


def show_memory():

    print("---- MEMORY ----")

    print("App:", memory.get_app())
    print("Window:", memory.get_window())
    print("Site:", memory.get_site())
    print("File:", memory.get_file())
    print("Action:", memory.get_action())

    print("----------------")


def get_command():

    global voice_mode, jarvis_mode

    if jarvis_mode:
        text = listen_once()
        return text if text else ""

    if voice_mode:
        text = listen_once()
        return text if text else ""

    return input(">>> ").strip()


def start_fury():

    global voice_mode, jarvis_mode

    print("=================================")
    print("🔥 FURY AI ASSISTANT STARTED")
    print("voice mode / jarvis mode / exit")
    print("=================================")

    register_all_agents()

    while True:

        command = get_command()

        if not command:
            continue

        cmd = command.lower()

        if cmd == "exit":
            speak("Shutting down")
            print("Shutting down Fury")
            break

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

        if command.startswith("goal "):

            goal = command.replace("goal ", "")

            speak("Goal mode")

            jarvis.run_loop(goal)

            continue

        if command.startswith("auto "):

            goal = command.replace("auto ", "")

            speak("Autonomous mode")

            run_autonomous(goal)

            continue

        # ---------- NORMAL ----------

        plan = create_plan(command)

        print("\nExecution Plan:")

        if isinstance(plan, dict):
            print(plan)
        else:
            for step in plan:
                print(step)

        speak("Executing")

        # FIX-1
        final_core.execute(plan)

        speak("Done")

        show_memory()


if __name__ == "__main__":
    start_fury()

    