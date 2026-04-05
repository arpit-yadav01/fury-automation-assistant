import time

from automation.ui_engine import type_text, press, hotkey, wait, click
from automation.software_control import open_application
from automation.window_manager import focus_window
from automation.file_manager import create_file

from developer.terminal_engine import run_terminal_command
from browser.browser_agent import open_website

from brain.context_memory import memory
from skills.skill_manager import execute_skill


MAX_STEP_RETRY = 2


def run_workflow(steps):

    if not steps:
        print("No workflow steps")
        return

    print("Running workflow...")

    for step in steps:

        retry = 0

        while retry <= MAX_STEP_RETRY:

            try:

                action = step.get("action")

                print("STEP:", step)

                # -----------------------
                # OPEN APP
                # -----------------------
                if action == "open_app":

                    name = step["name"]

                    open_application(name)

                    wait(3)

                    focus_window(name)

                    memory.set_app(name)
                    memory.set_window(name)
                    memory.set_action("open_app")

                    break

                # -----------------------
                # OPEN URL
                # -----------------------
                elif action == "open_url":

                    url = step["url"]

                    open_website(url)

                    wait(4)

                    focus_window("chrome")

                    memory.set_site(
                        "youtube" if "youtube" in url else "google"
                    )
                    memory.set_app("browser")
                    memory.set_window("chrome")
                    memory.set_action("open_website")

                    break

                # -----------------------
                # WAIT
                # -----------------------
                elif action == "wait":

                    wait(step.get("time", 1))
                    break

                # -----------------------
                # TYPE (🔥 FIXED)
                # -----------------------
                elif action == "type":

                    app = memory.get_app()

                    # ✅ JUST FOCUS + TYPE (NO OCR CLICK)
                    if app == "browser":
                        focus_window("chrome")
                        wait(0.5)

                    else:
                        win = memory.get_window()
                        if win:
                            focus_window(win)
                            wait(0.5)

                    print("Typing:", step["text"])

                    type_text(step["text"])

                    memory.set_action("type_text")

                    break

                # -----------------------
                # PRESS
                # -----------------------
                elif action == "press":

                    press(step["key"])
                    break

                # -----------------------
                # HOTKEY
                # -----------------------
                elif action == "hotkey":

                    hotkey(*step["keys"])
                    break

                # -----------------------
                # CLICK
                # -----------------------
                elif action == "click":

                    click()
                    break

                # -----------------------
                # CREATE FILE
                # -----------------------
                elif action == "create_file":

                    path = step["path"]

                    create_file(path)

                    memory.set_file(path)
                    memory.set_action("create_file")

                    break

                # -----------------------
                # TERMINAL
                # -----------------------
                elif action == "terminal":

                    run_terminal_command(step["cmd"])

                    memory.set_action("run_terminal")

                    break

                # -----------------------
                # SKILL
                # -----------------------
                elif action == "skill":

                    task = step.get("data")

                    if task:

                        ok = execute_skill(task)

                        if ok:
                            break

                    raise Exception("Skill failed")

                else:

                    raise Exception("Unknown action")

            except Exception as e:

                retry += 1

                print("Step error:", e, "Retry:", retry)

                if retry > MAX_STEP_RETRY:
                    print("Skipping step")
                    break

from brain.command_parser import parse_command
from brain.llm_brain import interpret_with_llm
from brain.ai_interpreter import interpret_command

from brain.context_memory import memory


print("🔥 USING FINAL TASK PLANNER")


# -------------------------
# SPLIT COMMAND
# -------------------------

def split_command(command):

    command = command.replace(",", " and ")

    parts = command.split(" and ")

    return [p.strip() for p in parts if p.strip()]


# -------------------------
# APPLY CONTEXT
# -------------------------

def apply_context(task):

    intent = task.get("intent")

    win = memory.get_window()
    app = memory.get_app()
    site = memory.get_site()

    if intent == "type_text":

        if win:
            task["window"] = win
        elif app == "browser":
            task["window"] = "chrome"
        elif app:
            task["window"] = app

    if intent == "web_search":

        if not task.get("site") and site:
            task["site"] = site

    return task


# =========================
# 🔥 BUILD WORKFLOW (FINAL CORRECT)
# =========================

def build_workflow(tasks):

    steps = []

    current_site = memory.get_site()

    for t in tasks:

        t = apply_context(t)

        intent = t.get("intent")

        # -----------------------
        # OPEN APP
        # -----------------------
        if intent == "open_app":

            app = t.get("app")

            steps.append({
                "action": "open_app",
                "name": app
            })

        # -----------------------
        # OPEN WEBSITE (🔥 IMPORTANT FIX)
        # -----------------------
        elif intent == "open_website":

            url = t.get("url")

            steps.append({
                "action": "open_url",
                "url": url
            })

            # 🔥 update context
            if "youtube" in url:
                current_site = "youtube"
            elif "google" in url:
                current_site = "google"

        # -----------------------
        # WEB SEARCH (🔥 FINAL FIX)
        # -----------------------
        elif intent == "web_search":

            query = t.get("query")

            # 🔥 USE CONTEXT FIRST
            site = t.get("site") or current_site or "google"

            # -------------------
            # YOUTUBE SEARCH
            # -------------------
            if site == "youtube":

                # ⚠️ DO NOT open youtube again if already opened
                if current_site != "youtube":
                    steps.append({
                        "action": "open_url",
                        "url": "https://www.youtube.com"
                    })
                    steps.append({"action": "wait", "time": 3})

                steps.append({"action": "press", "key": "/"})
                steps.append({"action": "wait", "time": 1})
                steps.append({"action": "type", "text": query})
                steps.append({"action": "press", "key": "enter"})

            # -------------------
            # GOOGLE SEARCH
            # -------------------
            else:

                if current_site != "google":
                    steps.append({
                        "action": "open_url",
                        "url": "https://www.google.com"
                    })
                    steps.append({"action": "wait", "time": 2})

                steps.append({"action": "type", "text": query})
                steps.append({"action": "press", "key": "enter"})

        # -----------------------
        # TYPE
        # -----------------------
        elif intent == "type_text":

            steps.append({
                "action": "type",
                "text": t.get("text")
            })

        # -----------------------
        # FALLBACK
        # -----------------------
        else:

            steps.append({
                "action": "skill",
                "data": t
            })

    return {"workflow": steps}


# =========================
# MAIN
# =========================

def create_plan(command):

    parts = split_command(command)

    tasks = []

    for part in parts:

        task = parse_command(part)

        if task:
            tasks.append(task)

    # -----------------------
    # MULTI STEP
    # -----------------------
    if len(tasks) > 1:
        print("Planner: building workflow")
        return build_workflow(tasks)

    # -----------------------
    # SINGLE STEP
    # -----------------------
    if tasks:
        return tasks

    # -----------------------
    # AI FALLBACK
    # -----------------------
    ai_result = interpret_command(command)

    if ai_result:
        return [ai_result]

    llm_tasks = interpret_with_llm(command)

    if llm_tasks:
        return llm_tasks

    return [{"intent": "unknown"}]                