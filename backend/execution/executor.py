from automation.software_control import open_application
from automation.typing_engine import type_text
from automation.file_manager import create_file
from developer.code_generator import generate_code
from automation.window_manager import focus_window
from developer.terminal_engine import run_terminal_command
from browser.browser_agent import open_website

def execute_plan(plan):

    last_app = None

    for task in plan:

        intent = task["intent"]

        if intent == "open_app":

            app = task["app"]

            print("Opening", app)

            open_application(app)

            last_app = app

            focus_window(app.capitalize())


        elif intent == "type_text":

            text = task["text"]

            if last_app:
                focus_window(last_app.capitalize())

            print("Typing:", text)

            type_text(text)


        elif intent == "create_file":

            filename = task["filename"]

            create_file(filename)


        elif intent == "generate_code":

            language = task["language"]
            task_name = task["task"]

            print("Generating code...")

            code = generate_code(language, task_name)

            type_text(code)


        elif intent == "run_terminal":

            command = task["command"]

            print("Executing terminal command:", command)

            run_terminal_command(command)

        elif intent == "open_website":

            url = task["url"]

            print("Opening website:", url)

            open_website(url)


        else:

            print("Unknown task:", task)