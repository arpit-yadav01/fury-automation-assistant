


# # skills/skills_registry.py

# from browser.browser_agent import open_website, smart_search
# from automation.file_manager import create_file, write_to_file
# from developer.terminal_engine import run_terminal_command
# from vision.ui_click import click_text
# from automation.typing_engine import type_text, smart_type
# from automation.software_control import open_application
# from brain.context_memory import memory

# from skills.auto_skill_builder import build_auto_skills

# from developer.dev_workflow import (
#     open_vscode,
#     create_new_file,
#     write_code,
#     save_file,
#     run_python_file,
#     run_command,
# )


# # -------------------------
# # OPEN APP
# # -------------------------

# def skill_open_app(task):

#     app = task.get("app")

#     if not app:
#         return

#     open_application(app)

#     memory.set_app(app)

#     if app == "vscode":
#         memory.set_window("code")
#     elif app == "notepad":
#         memory.set_window("notepad")
#     else:
#         memory.set_window(app)

#     memory.set_action("open_app")


# # -------------------------
# # OPEN WEBSITE
# # -------------------------

# def skill_open_website(task):

#     url = task.get("url")

#     if not url:
#         return

#     open_website(url)

#     memory.set_site(url)
#     memory.set_app("browser")
#     memory.set_window("chrome")
#     memory.set_action("open_website")


# # -------------------------
# # WEB SEARCH
# # -------------------------

# def skill_web_search(task):

#     query = task.get("query")

#     if not query:
#         open_website("https://google.com")
#         return

#     smart_search(query)

#     memory.set_action("web_search")


# # -------------------------
# # CREATE FILE
# # -------------------------

# def skill_create_file(task):

#     filename = task.get("filename")

#     if filename:
#         create_file(filename)
#         memory.set_file(filename)
#         memory.set_action("create_file")


# # -------------------------
# # WRITE FILE
# # -------------------------

# def skill_write_file(task):

#     filename = task.get("filename")
#     text = task.get("text")

#     if filename and text:
#         write_to_file(filename, text)


# # -------------------------
# # TYPE TEXT
# # -------------------------

# def skill_type_text(task):

#     text = task.get("text")
#     window = task.get("window")

#     if not text:
#         return

#     if window:
#         smart_type(text, window)
#     else:
#         type_text(text)

#     memory.set_action("type_text")


# # -------------------------
# # TERMINAL
# # -------------------------

# def skill_run_terminal(task):

#     command = task.get("command")

#     if command:
#         run_terminal_command(command)
#         memory.set_action("run_terminal")


# # -------------------------
# # CLICK
# # -------------------------

# def skill_click_text(task):

#     text = task.get("text")

#     if text:
#         click_text(text)


# # -------------------------
# # DEV SKILLS
# # -------------------------

# def skill_open_vscode(task):
#     open_vscode()


# def skill_create_code_file(task):

#     filename = task.get("filename", "test.py")
#     create_new_file(filename)


# def skill_write_code(task):

#     code = task.get("code")

#     if code:
#         write_code(code)


# def skill_save_file(task):
#     save_file()


# def skill_run_python(task):

#     filename = task.get("filename", "test.py")
#     run_python_file(filename)


# def skill_dev_command(task):

#     cmd = task.get("command")

#     if cmd:
#         run_command(cmd)


# # =========================
# # 🔥 EXECUTE SKILL (FIXED)
# # =========================

# def execute_skill(intent, task):

#     # -------------------------
#     # AUTO SKILLS
#     # -------------------------

#     auto = build_auto_skills()

#     if intent in auto:

#         print("⚡ Using learned skill:", intent)

#         return {
#             "workflow": auto[intent]
# }

#     # -------------------------
#     # NORMAL SKILLS
#     # -------------------------

#     skill = SKILLS.get(intent)

#     if skill:
#         return skill(task)

#     print("Skill not found:", intent)


# # -------------------------
# # MAP
# # -------------------------

# SKILLS = {

#     "open_app": skill_open_app,
#     "open_website": skill_open_website,
#     "web_search": skill_web_search,
#     "create_file": skill_create_file,
#     "write_file": skill_write_file,
#     "type_text": skill_type_text,
#     "run_terminal": skill_run_terminal,
#     "click_text": skill_click_text,

#     "open_vscode": skill_open_vscode,
#     "create_code_file": skill_create_code_file,
#     "write_code": skill_write_code,
#     "save_file": skill_save_file,
#     "run_python": skill_run_python,
#     "run_dev_command": skill_dev_command,
# }


from browser.browser_agent import open_website, smart_search
from automation.file_manager import create_file, write_to_file
from developer.terminal_engine import run_terminal_command
from vision.ui_click import click_text
from automation.typing_engine import type_text, smart_type
from automation.software_control import open_application
from automation.window_manager import focus_window
from automation.ui_engine import wait
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
        return True


# -------------------------
# WRITE FILE
# -------------------------

def skill_write_file(task):

    filename = task.get("filename")
    text = task.get("text")

    if filename and text:
        write_to_file(filename, text)
        return True


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
    return True


# -------------------------
# WRITE CODE (AI POWERED)
# -------------------------

def skill_write_code_task(task):

    task_text = task.get("task") or task.get("text") or task.get("code")
    filename = task.get("filename")

    if not task_text:
        print("No task for write_code")
        return False

    # generate code
    from brain.llm_brain import generate_code

    print(f"Generating code for: {task_text}")

    code = generate_code(task_text)

    if not code:
        code = f"# {task_text}\npass\n"

    print(f"Writing code ({len(code)} chars)")

    # ✅ if we have a filename, write directly to disk — no window needed
    if filename:

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)

            print(f"✅ Code written to file: {filename}")
            memory.set_file(filename)
            memory.set_action("write_code")
            return True

        except Exception as e:
            print(f"File write error: {e}")
            # fall through to window typing

    # ✅ no filename — type into active window
    win = memory.get_window()

    if win:
        focus_window(win)

    wait(0.5)
    type_text(code)
    memory.set_action("write_code")
    return True


# -------------------------
# TERMINAL
# -------------------------

def skill_run_terminal(task):

    command = task.get("command")

    if command:
        run_terminal_command(command)
        memory.set_action("run_terminal")
        return True


# -------------------------
# CLICK
# -------------------------

def skill_click_text(task):

    text = task.get("text")

    if text:
        click_text(text)
        return True


# -------------------------
# DEV SKILLS
# -------------------------

def skill_open_vscode(task):
    open_vscode()
    return True


def skill_create_code_file(task):
    filename = task.get("filename", "test.py")
    create_new_file(filename)
    return True


def skill_write_code_dev(task):
    code = task.get("code")
    if code:
        write_code(code)
        return True


def skill_save_file(task):
    save_file()
    return True


def skill_run_python(task):
    filename = task.get("filename", "test.py")
    run_python_file(filename)
    return True


def skill_dev_command(task):
    cmd = task.get("command")
    if cmd:
        run_command(cmd)
        return True


# =========================
# EXECUTE SKILL
# =========================

def execute_skill(task):

    if not isinstance(task, dict):
        print("execute_skill: task is not dict")
        return False

    intent = task.get("intent")

    if not intent:
        print("No intent in task")
        return False

    # -------------------------
    # AUTO SKILLS
    # -------------------------

    auto = build_auto_skills()

    if intent in auto:
        print("⚡ Using learned skill:", intent)
        from execution.workflow_engine import run_workflow
        run_workflow(auto[intent])
        return True

    # -------------------------
    # NORMAL SKILLS
    # -------------------------

    skill = SKILLS.get(intent)

    if skill:
        print("Executing skill:", intent)
        result = skill(task)
        memory.set_action(intent)
        return True

    print("No skill found for:", intent)
    return False


# -------------------------
# SKILLS MAP
# -------------------------

SKILLS = {

    "open_app":         skill_open_app,
    "open_website":     skill_open_website,
    "web_search":       skill_web_search,
    "create_file":      skill_create_file,
    "write_file":       skill_write_file,
    "type_text":        skill_type_text,
    "write_code":       skill_write_code_task,   # ✅ AI powered
    "run_terminal":     skill_run_terminal,
    "click_text":       skill_click_text,

    "open_vscode":      skill_open_vscode,
    "create_code_file": skill_create_code_file,
    "write_code_dev":   skill_write_code_dev,
    "save_file":        skill_save_file,
    "run_python":       skill_run_python,
    "run_dev_command":  skill_dev_command,
}