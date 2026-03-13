# skills/skills_registry.py

from browser.browser_agent import open_website, search_on_page
from automation.file_manager import create_file, write_to_file
from developer.terminal_engine import run_terminal_command
from vision.ui_click import click_text
from automation.typing_engine import type_text
from automation.software_control import open_application


# -------------------------
# SKILLS
# -------------------------

def skill_open_app(task):

    app = task.get("app")

    if app:
        print("Opening", app)
        open_application(app)


def skill_open_website(task):

    url = task.get("url")

    if url:
        print("Opening website:", url)
        open_website(url)


def skill_web_search(task):

    query = task.get("query")
    site = task.get("site", "google")

    if not query:
        return

    if site == "youtube":

        open_website("https://www.youtube.com")
        search_on_page(query)

    else:

        open_website(f"https://www.google.com/search?q={query}")


def skill_create_file(task):

    filename = task.get("filename")

    if filename:
        create_file(filename)


def skill_write_file(task):

    filename = task.get("filename")
    text = task.get("text")

    if filename and text:
        write_to_file(filename, text)


def skill_type_text(task):

    text = task.get("text")

    if text:
        type_text(text)


def skill_run_terminal(task):

    command = task.get("command")

    if command:
        run_terminal_command(command)


def skill_click_text(task):

    text = task.get("text")

    if text:
        click_text(text)


# -------------------------
# SKILL MAP
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

}