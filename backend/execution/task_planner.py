from brain.command_parser import parse_command
from brain.llm_brain import interpret_with_llm
from brain.ai_interpreter import interpret_command

from brain.context_memory import memory


print("🔥 FINAL TASK PLANNER (LOCKED CONTEXT)")


# -------------------------
# SPLIT COMMAND
# -------------------------

def split_command(command):
    command = command.replace(",", " and ")
    return [p.strip() for p in command.split(" and ") if p.strip()]


# -------------------------
# APPLY CONTEXT
# -------------------------

def apply_context(task):

    if task.get("intent") == "web_search":

        # 🔥 FORCE USE MEMORY SITE
        site = memory.get_site()

        if site:
            task["site"] = site

    return task


# =========================
# BUILD WORKFLOW (FINAL FIX)
# =========================

def build_workflow(tasks):

    steps = []
    current_site = None

    for t in tasks:

        t = apply_context(t)
        intent = t.get("intent")

        # -----------------------
        # OPEN WEBSITE
        # -----------------------
        if intent == "open_website":

            url = t.get("url")

            steps.append({
                "action": "open_url",
                "url": url
            })

            # 🔥 LOCK SITE
            if "youtube" in url:
                current_site = "youtube"
            elif "google" in url:
                current_site = "google"

        # -----------------------
        # WEB SEARCH (🔥 FIXED)
        # -----------------------
        elif intent == "web_search":

            query = t.get("query")

            # 🔥 STRICT SITE CONTROL
            site = t.get("site") or current_site

            if not site:
                site = "google"

            # -------------------
            # YOUTUBE SEARCH
            # -------------------
            if site == "youtube":

                # ❌ DO NOT OPEN GOOGLE
                # ❌ DO NOT OVERRIDE

                steps.append({"action": "wait", "time": 2})
                steps.append({"action": "press", "key": "/"})
                steps.append({"action": "wait", "time": 1})
                steps.append({"action": "type", "text": query})
                steps.append({"action": "press", "key": "enter"})

            # -------------------
            # GOOGLE SEARCH
            # -------------------
            else:

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

    if len(tasks) > 1:
        print("Planner: building workflow")
        return build_workflow(tasks)

    if tasks:
        return tasks

    ai_result = interpret_command(command)
    if ai_result:
        return [ai_result]

    llm_tasks = interpret_with_llm(command)
    if llm_tasks:
        return llm_tasks

    return [{"intent": "unknown"}]