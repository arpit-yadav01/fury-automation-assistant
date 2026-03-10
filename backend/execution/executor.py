# execution/executor.py

from automation.software_control import open_application
from automation.typing_engine import type_text
from automation.file_manager import create_file
from developer.code_generator import generate_code
from automation.window_manager import focus_window
from developer.terminal_engine import run_terminal_command
from browser.browser_agent import open_website, search_on_page


def execute_plan(plan):

    last_app = None
    last_site = None

    for task in plan:

        intent = task["intent"]

        # -----------------------------
        # OPEN APPLICATION
        # -----------------------------
        if intent == "open_app":

            app = task["app"]

            print("Opening", app)

            open_application(app)

            last_app = app

            focus_window(app.capitalize())

        # -----------------------------
        # TYPE TEXT
        # -----------------------------
        elif intent == "type_text":

            text = task["text"]

            if last_app:
                focus_window(last_app.capitalize())

            print("Typing:", text)

            type_text(text)

        # -----------------------------
        # CREATE FILE
        # -----------------------------
        elif intent == "create_file":

            filename = task["filename"]

            create_file(filename)

        # -----------------------------
        # GENERATE CODE
        # -----------------------------
        elif intent == "generate_code":

            language = task["language"]
            task_name = task["task"]

            print("Generating code...")

            code = generate_code(language, task_name)

            type_text(code)

        # -----------------------------
        # TERMINAL COMMAND
        # -----------------------------
        elif intent == "run_terminal":

            command = task["command"]

            print("Executing terminal command:", command)

            run_terminal_command(command)

        # -----------------------------
        # OPEN WEBSITE
        # -----------------------------
        elif intent == "open_website":

            url = task["url"]

            print("Opening website:", url)

            open_website(url)

            if "youtube" in url:
                last_site = "youtube"

            elif "google" in url:
                last_site = "google"

        # -----------------------------
        # WEB SEARCH
        # -----------------------------
        elif intent == "web_search":

            query = task["query"]
            site = task.get("site")

            # If previous site was YouTube, override Google search
            if site == "google" and last_site == "youtube":
                site = "youtube"

            if site == "youtube":

                print("Searching YouTube:", query)

                search_on_page(query, "input#search")

            else:

                print("Searching Google:", query)

                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

                open_website(search_url)

        # -----------------------------
        # UNKNOWN TASK
        # -----------------------------
        else:

            print("Unknown task:", task)