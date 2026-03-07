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

        elif intent == "write_code":

            print("Writing python code")

            code = "print('Hello World')"

            type_text(code)

        else:

            print("Unknown task:", task)