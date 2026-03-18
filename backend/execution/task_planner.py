# execution/task_planner.py

from brain.command_parser import parse_command
from brain.llm_brain import interpret_with_llm
from brain.ai_interpreter import interpret_command


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
# helper — build workflow
# -----------------------------
def build_workflow(tasks):

    steps = []

    i = 0

    while i < len(tasks):

        t = tasks[i]
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

            # check next step for typing (search case)
            if i + 1 < len(tasks):

                next_task = tasks[i + 1]

                if next_task.get("intent") == "type_text":

                    text = next_task.get("text")

                    steps.append({
                        "action": "wait",
                        "time": 3
                    })

                    steps.append({
                        "action": "type",
                        "text": text
                    })

                    steps.append({
                        "action": "press",
                        "key": "enter"
                    })

                    i += 1  # skip next task


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
        return [ai_result]


    # -----------------------------
    # 2. LLM
    # -----------------------------

    llm_tasks = interpret_with_llm(command)

    if llm_tasks:
        return llm_tasks


    # -----------------------------
    # 3. split command
    # -----------------------------

    parts = split_command(command)

    tasks = []

    for part in parts:

        task = parse_command(part)

        if task:
            tasks.append(task)


    # -----------------------------
    # 4. single task
    # -----------------------------

    if len(tasks) == 1:
        return tasks


    # -----------------------------
    # 5. multi task → workflow
    # -----------------------------

    if len(tasks) > 1:

        print("Planner: building workflow")

        return build_workflow(tasks)


    # -----------------------------

    return [{"intent": "unknown"}]