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

    # -------------------------
    # TYPE TEXT CONTEXT
    # -------------------------

    if intent == "type_text":

        # if last site exists → convert to search
        if site:

            if "youtube" in site:
                task["intent"] = "web_search"
                task["site"] = "youtube"
                task["query"] = task.get("text")
                return task

            if "google" in site:
                task["intent"] = "web_search"
                task["site"] = "google"
                task["query"] = task.get("text")
                return task

        # otherwise normal typing
        if win:
            task["window"] = win
        elif app:
            task["window"] = app

    # -------------------------
    # TERMINAL CONTEXT
    # -------------------------

    if intent == "run_terminal":

        if win:
            task["window"] = win
        elif app:
            task["window"] = app

    # -------------------------
    # SEARCH CONTEXT
    # -------------------------

    if intent == "web_search":

        if not task.get("site"):

            if site:
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

            url = t.get("url")

            steps.append({
                "action": "open_url",
                "url": url
            })

        # -----------------------
        # TYPE
        # -----------------------

        elif intent == "type_text":

            steps.append({
                "action": "type",
                "text": t.get("text")
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

        # -----------------------
        # FALLBACK
        # -----------------------

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

    # -----------------------------
    # 1. AI interpreter
    # -----------------------------

    ai_result = interpret_command(command)

    if ai_result:
        return [apply_context(ai_result)]

    # -----------------------------
    # 2. LLM
    # -----------------------------

    llm_tasks = interpret_with_llm(command)

    if llm_tasks:
        return [apply_context(t) for t in llm_tasks]

    # -----------------------------
    # 3. split command
    # -----------------------------

    parts = split_command(command)

    tasks = []

    for part in parts:

        task = parse_command(part)

        if task:
            task = apply_context(task)
            tasks.append(task)

    # -----------------------------
    # single
    # -----------------------------

    if len(tasks) == 1:
        return tasks

    # -----------------------------
    # workflow
    # -----------------------------

    if len(tasks) > 1:

        print("Planner: building workflow")

        return build_workflow(tasks)

    return [{"intent": "unknown"}]