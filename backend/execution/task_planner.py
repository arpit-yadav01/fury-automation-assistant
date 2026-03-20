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