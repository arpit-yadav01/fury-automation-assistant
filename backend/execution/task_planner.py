# from brain.command_parser import parse_command
# from brain.llm_brain import interpret_with_llm
# from brain.ai_interpreter import interpret_command

# from brain.context_memory import memory
# from memory.experience_memory import find_similar

# print("🔥 FINAL TASK PLANNER (PHASE-7 COMPLETE)")


# # -------------------------
# # SPLIT COMMAND (IMPROVED)
# # -------------------------

# def split_command(command):

#     command = command.replace(",", " and ")
#     command = command.replace(" then ", " and ")

#     return [p.strip() for p in command.split(" and ") if p.strip()]


# # -------------------------
# # APPLY CONTEXT
# # -------------------------

# def apply_context(task):

#     if task.get("intent") == "web_search":

#         site = memory.get_site()

#         if site:
#             task["site"] = site

#     return task


# # =========================
# # BUILD WORKFLOW
# # =========================

# def build_workflow(tasks):

#     steps = []
#     current_site = None

#     for t in tasks:

#         t = apply_context(t)
#         intent = t.get("intent")

#         # -----------------------
#         # OPEN WEBSITE
#         # -----------------------
#         if intent == "open_website":

#             url = t.get("url")

#             steps.append({
#                 "action": "open_url",
#                 "url": url
#             })

#             if "youtube" in url:
#                 current_site = "youtube"
#             elif "google" in url:
#                 current_site = "google"

#         # -----------------------
#         # WEB SEARCH
#         # -----------------------
#         elif intent == "web_search":

#             query = t.get("query")

#             site = t.get("site") or current_site

#             if not site:
#                 site = "google"

#             # YOUTUBE
#             if site == "youtube":

#                 steps.append({"action": "wait", "time": 2})
#                 steps.append({"action": "press", "key": "/"})
#                 steps.append({"action": "wait", "time": 1})
#                 steps.append({"action": "type", "text": query})
#                 steps.append({"action": "press", "key": "enter"})

#             # GOOGLE
#             else:

#                 steps.append({
#                     "action": "open_url",
#                     "url": "https://www.google.com"
#                 })

#                 steps.append({"action": "wait", "time": 2})
#                 steps.append({"action": "type", "text": query})
#                 steps.append({"action": "press", "key": "enter"})

#         # -----------------------
#         # TYPE
#         # -----------------------
#         elif intent == "type_text":

#             steps.append({
#                 "action": "type",
#                 "text": t.get("text")
#             })

#         # -----------------------
#         # FALLBACK
#         # -----------------------
#         else:

#             steps.append({
#                 "action": "skill",
#                 "data": t
#             })

#     return {"workflow": steps}


# # =========================
# # SMART SINGLE COMMAND FIX
# # =========================

# def handle_single_task(task):

#     intent = task.get("intent")

#     # 🔥 FIX 1 — search command
#     if intent == "web_search":
#         return build_workflow([task])

#     # 🔥 FIX 2 — open youtube search pattern
#     raw = task.get("raw", "").lower()

#     if "youtube" in raw and "search" in raw:

#         query = raw.replace("open youtube", "").replace("search", "").strip()

#         return build_workflow([
#             {"intent": "open_website", "url": "https://www.youtube.com"},
#             {"intent": "web_search", "query": query, "site": "youtube"}
#         ])

#     # 🔥 FIX 3 — open app safe execution
#     if intent == "open_app":
#         return {"workflow": [{"action": "skill", "data": task}]}

#     return [task]


# # =========================
# # MAIN
# # =========================

# def create_plan(command):

#     parts = split_command(command)

#     tasks = []

#     for part in parts:

#         task = parse_command(part)

#         if task:
#             tasks.append(task)

#     # -----------------------
#     # MULTI STEP
#     # -----------------------
#     if len(tasks) > 1:
#         print("Planner: building workflow")
#         return build_workflow(tasks)

#     # -----------------------
#     # SINGLE STEP (🔥 FIX)
#     # -----------------------
#     if tasks:
#         return handle_single_task(tasks[0])

#     # -----------------------
#     # AI FALLBACK
#     # -----------------------
#     ai_result = interpret_command(command)

#     if ai_result:
#         return handle_single_task(ai_result)

#     llm_tasks = interpret_with_llm(command)

#     if llm_tasks:
#         return build_workflow(llm_tasks)

#     return [{"intent": "unknown"}]




from brain.command_parser import parse_command
from brain.llm_brain import interpret_with_llm
from brain.ai_interpreter import interpret_command

from brain.context_memory import memory
from memory.experience_memory import find_similar

print("🔥 FINAL TASK PLANNER (PHASE-8 READY)")


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
    # 🔥 STEP 103 — MEMORY CHECK
    # =========================

    exp = find_similar(command)

    if exp and exp.get("success"):
        print("⚡ Using past experience")
        return exp.get("plan")

    # -------------------------
    # NORMAL FLOW
    # -------------------------

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