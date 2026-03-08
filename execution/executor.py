# execution/executor.py

from automation.software_control import open_application
from automation.typing_engine import type_text


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

        else:

            print("Unknown task:", task)