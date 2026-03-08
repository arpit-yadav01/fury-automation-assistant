# execution/executor.py

from automation.software_control import open_application
from automation.typing_engine import type_text
from automation.file_manager import create_file


def execute_plan(plan):

    for task in plan:

        intent = task["intent"]

        if intent == "open_app":

            app = task["app"]

            print("Opening", app)

            open_application(app)

        elif intent == "type_text":

            text = task["text"]

            print("Typing:", text)

            type_text(text)

        elif intent == "create_file":

            filename = task["filename"]

            create_file(filename)

        else:

            print("Unknown task:", task)