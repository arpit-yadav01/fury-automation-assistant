
# # execution/task_planner.py
# # STEP 112 — multi_plan() added as final fallback before unknown

# from brain.command_parser import parse_command
# from brain.llm_brain import interpret_with_llm
# from brain.ai_interpreter import interpret_command

# from brain.context_memory import memory
# from memory.experience_memory import find_similar
# from skills.auto_skill_builder import find_best_skill

# # STEP 112
# from execution.planner_v2 import multi_plan

# print("🔥 FINAL TASK PLANNER (PHASE-9 STEP-112)")


# def split_command(command):
#     command = command.replace(",", " and ")
#     command = command.replace(" then ", " and ")
#     return [p.strip() for p in command.split(" and ") if p.strip()]


# def apply_context(task, current_site=None):
#     if task.get("intent") == "web_search":
#         if not task.get("site"):
#             site = current_site or memory.get_site()
#             if site:
#                 task["site"] = site
#     return task


# def build_workflow(tasks):

#     steps = []
#     current_site = None
#     current_file = None

#     for t in tasks:

#         t = apply_context(t, current_site)
#         intent = t.get("intent")

#         if intent == "open_website":

#             url = t.get("url")
#             steps.append({"action": "open_url", "url": url})

#             if "youtube" in url:
#                 current_site = "youtube"
#             elif "google" in url:
#                 current_site = "google"
#             else:
#                 current_site = url

#         elif intent == "web_search":

#             query = t.get("query", "")
#             site = t.get("site") or current_site or "google"
#             query_encoded = query.replace(" ", "+")

#             if site == "youtube":
#                 steps.append({
#                     "action": "open_url",
#                     "url": f"https://www.youtube.com/results?search_query={query_encoded}"
#                 })
#             else:
#                 steps.append({
#                     "action": "open_url",
#                     "url": f"https://www.google.com/search?q={query_encoded}"
#                 })

#         elif intent == "type_text":
#             steps.append({"action": "type", "text": t.get("text")})

#         elif intent == "create_file":
#             filename = t.get("filename")
#             current_file = filename
#             steps.append({"action": "create_file", "path": filename})

#         elif intent == "write_code":
#             steps.append({
#                 "action": "skill",
#                 "data": {
#                     "intent": "write_code",
#                     "task": t.get("task"),
#                     "filename": current_file,
#                 }
#             })

#         elif intent == "open_app":
#             # ✅ use open_app action directly so workflow_engine handles it
#             steps.append({
#                 "action": "open_app",
#                 "name": t.get("app")
#             })

#         else:
#             steps.append({"action": "skill", "data": t})

#     return {"workflow": steps}


# def handle_single_task(task):

#     intent = task.get("intent")

#     if intent == "web_search":
#         return build_workflow([task])

#     raw = task.get("raw", "").lower()

#     if "youtube" in raw and ("search" in raw or "type" in raw):

#         query = raw
#         for w in ["open youtube", "youtube", "search", "type"]:
#             query = query.replace(w, "")
#         query = query.strip()

#         return build_workflow([
#             {"intent": "open_website", "url": "https://www.youtube.com"},
#             {"intent": "web_search", "query": query, "site": "youtube"}
#         ])

#     if intent == "open_app":
#         return {"workflow": [{"action": "open_app", "name": task.get("app")}]}

#     if intent == "create_file":
#         return build_workflow([task])

#     if intent == "write_code":
#         return build_workflow([task])

#     return [task]


# def create_plan(command):

#     # -------------------------
#     # SMART SKILL (exact match)
#     # -------------------------
#     skill_name, plan = find_best_skill(command)

#     if plan and len(command.split()) <= 4:

#         print(f"⚡ Smart skill used: {skill_name}")

#         if isinstance(plan, dict) and "workflow" in plan:
#             return plan

#         if isinstance(plan, list):
#             return {"workflow": plan}

#     # -------------------------
#     # PAST EXPERIENCE
#     # -------------------------
#     exp = find_similar(command)

#     if exp and exp.get("success"):

#         plan = exp.get("plan")

#         if isinstance(plan, str):
#             print("⚠️ Skipping bad cached plan")

#         else:
#             print("⚡ Using past experience")

#             if isinstance(plan, dict) and "workflow" in plan:
#                 return plan

#             if isinstance(plan, list):
#                 return {"workflow": plan}

#             if isinstance(plan, dict):
#                 return {"workflow": [plan]}

#     # -------------------------
#     # NORMAL PARSER FLOW
#     # -------------------------
#     parts = split_command(command)
#     tasks = []

#     for part in parts:
#         task = parse_command(part)
#         if task:
#             tasks.append(task)

#     if len(tasks) > 1:
#         print("Planner: building workflow")
#         return build_workflow(tasks)

#     if tasks:
#         result = handle_single_task(tasks[0])
#         # only return if it's not unknown
#         if not _is_unknown(result):
#             return result

#     # -------------------------
#     # AI INTERPRETER
#     # -------------------------
#     ai_result = interpret_command(command)

#     if ai_result and not _is_unknown(ai_result):
#         return handle_single_task(ai_result)

#     # -------------------------
#     # LLM INTERPRET
#     # -------------------------
#     llm_tasks = interpret_with_llm(command)

#     if llm_tasks and not _is_unknown(llm_tasks):
#         return build_workflow(llm_tasks)

#     # -------------------------
#     # STEP 112 — MULTI-HYPOTHESIS PLANNER
#     # last resort before giving up
#     # -------------------------
#     print("Planner: falling back to PlannerV2 multi-hypothesis")
#     multi = multi_plan(command)

#     if multi:
#         return multi

#     # -------------------------
#     # TRULY UNKNOWN
#     # -------------------------
#     return [{"intent": "unknown"}]


# # -------------------------
# # HELPER
# # -------------------------

# def _is_unknown(result):
#     """Check if a plan resolved to unknown — don't return these early."""
#     if isinstance(result, list):
#         return all(
#             isinstance(r, dict) and r.get("intent") == "unknown"
#             for r in result
#         )
#     if isinstance(result, dict):
#         return result.get("intent") == "unknown"
#     return False





# execution/task_planner.py
# STEP 112 — multi_plan() added as final fallback before unknown
# FIX: build_workflow now skips non-dict items (strings from LLM)

from brain.command_parser import parse_command
from brain.llm_brain import interpret_with_llm
from brain.ai_interpreter import interpret_command

from brain.context_memory import memory
from memory.experience_memory import find_similar
from skills.auto_skill_builder import find_best_skill

# STEP 112
from execution.planner_v2 import multi_plan

print("🔥 FINAL TASK PLANNER (PHASE-9 STEP-112)")


def split_command(command):
    command = command.replace(",", " and ")
    command = command.replace(" then ", " and ")
    return [p.strip() for p in command.split(" and ") if p.strip()]


def apply_context(task, current_site=None):
    if not isinstance(task, dict):
        return task
    if task.get("intent") == "web_search":
        if not task.get("site"):
            site = current_site or memory.get_site()
            if site:
                task["site"] = site
    return task


def build_workflow(tasks):

    steps = []
    current_site = None
    current_file = None

    for t in tasks:

        # ✅ FIX: skip strings or non-dicts from LLM output
        if not isinstance(t, dict):
            continue

        t = apply_context(t, current_site)
        intent = t.get("intent")

        if intent == "open_website":

            url = t.get("url")
            if not url:
                continue
            steps.append({"action": "open_url", "url": url})

            if "youtube" in url:
                current_site = "youtube"
            elif "google" in url:
                current_site = "google"
            else:
                current_site = url

        elif intent == "web_search":

            query = t.get("query", "")
            site = t.get("site") or current_site or "google"
            query_encoded = query.replace(" ", "+")

            if site == "youtube":
                steps.append({
                    "action": "open_url",
                    "url": f"https://www.youtube.com/results?search_query={query_encoded}"
                })
            else:
                steps.append({
                    "action": "open_url",
                    "url": f"https://www.google.com/search?q={query_encoded}"
                })

        elif intent == "type_text":
            steps.append({"action": "type", "text": t.get("text")})

        elif intent == "create_file":
            filename = t.get("filename")
            current_file = filename
            steps.append({"action": "create_file", "path": filename})

        elif intent == "write_code":
            steps.append({
                "action": "skill",
                "data": {
                    "intent": "write_code",
                    "task": t.get("task"),
                    "filename": current_file,
                }
            })

        elif intent == "open_app":
            steps.append({
                "action": "open_app",
                "name": t.get("app")
            })

        else:
            steps.append({"action": "skill", "data": t})

    return {"workflow": steps}


def handle_single_task(task):

    intent = task.get("intent")

    if intent == "web_search":
        return build_workflow([task])

    raw = task.get("raw", "").lower()

    if "youtube" in raw and ("search" in raw or "type" in raw):

        query = raw
        for w in ["open youtube", "youtube", "search", "type"]:
            query = query.replace(w, "")
        query = query.strip()

        return build_workflow([
            {"intent": "open_website", "url": "https://www.youtube.com"},
            {"intent": "web_search", "query": query, "site": "youtube"}
        ])

    if intent == "open_app":
        return {"workflow": [{"action": "open_app", "name": task.get("app")}]}

    if intent == "create_file":
        return build_workflow([task])

    if intent == "write_code":
        return build_workflow([task])

    return [task]


def create_plan(command):

    # -------------------------
    # SMART SKILL
    # -------------------------
    skill_name, plan = find_best_skill(command)

    if plan and len(command.split()) <= 4:
        print(f"⚡ Smart skill used: {skill_name}")
        if isinstance(plan, dict) and "workflow" in plan:
            return plan
        if isinstance(plan, list):
            return {"workflow": plan}

    # -------------------------
    # PAST EXPERIENCE
    # -------------------------
    exp = find_similar(command)

    if exp and exp.get("success"):
        plan = exp.get("plan")
        if isinstance(plan, str):
            print("⚠️ Skipping bad cached plan")
        else:
            print("⚡ Using past experience")
            if isinstance(plan, dict) and "workflow" in plan:
                return plan
            if isinstance(plan, list):
                return {"workflow": plan}
            if isinstance(plan, dict):
                return {"workflow": [plan]}

    # -------------------------
    # NORMAL PARSER FLOW
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
        result = handle_single_task(tasks[0])
        if not _is_unknown(result):
            return result

    # -------------------------
    # AI INTERPRETER
    # -------------------------
    ai_result = interpret_command(command)
    if ai_result and not _is_unknown(ai_result):
        return handle_single_task(ai_result)

    # -------------------------
    # LLM INTERPRET
    # -------------------------
    llm_tasks = interpret_with_llm(command)

    if llm_tasks and not _is_unknown(llm_tasks):
        # ✅ FIX: filter out any strings before building workflow
        if isinstance(llm_tasks, list):
            llm_tasks = [t for t in llm_tasks if isinstance(t, dict)]
        if llm_tasks:
            return build_workflow(llm_tasks)

    # -------------------------
    # STEP 112 — MULTI-HYPOTHESIS PLANNER
    # -------------------------
    print("Planner: falling back to PlannerV2 multi-hypothesis")
    multi = multi_plan(command)
    if multi:
        return multi

    return [{"intent": "unknown"}]


def _is_unknown(result):
    if isinstance(result, list):
        return all(
            isinstance(r, dict) and r.get("intent") == "unknown"
            for r in result
        )
    if isinstance(result, dict):
        return result.get("intent") == "unknown"
    return False