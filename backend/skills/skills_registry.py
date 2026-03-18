# skills/skills_registry.py

from browser.browser_agent import open_website, search_on_page
from automation.file_manager import create_file, write_to_file
from developer.terminal_engine import run_terminal_command
from vision.ui_click import click_text
from automation.typing_engine import type_text, smart_type
from automation.software_control import open_application

from brain.context_memory import memory

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

    # better window names
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
    site = task.get("site", "google")

    if not query:
        open_website("https://google.com")
        return

    if site == "youtube":

        open_website("https://youtube.com")
        search_on_page(query)

    else:

        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        open_website(url)

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