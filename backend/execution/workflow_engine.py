# execution/workflow_engine.py

import time

from automation.ui_engine import type_text, press, hotkey, wait, click
from automation.software_control import open_application
from automation.window_manager import focus_window
from automation.file_manager import create_file

from developer.terminal_engine import run_terminal_command


def run_workflow(steps):

    if not steps:
        print("No workflow steps")
        return

    print("Running workflow...")

    for step in steps:

        action = step.get("action")

        print("STEP:", step)

        try:

            # -----------------------
            # OPEN APP
            # -----------------------
            if action == "open_app":

                name = step["name"]

                open_application(name)

                wait(2)

                focus_window(name)

                wait(1)


            # -----------------------
            # WAIT
            # -----------------------
            elif action == "wait":

                wait(step.get("time", 1))


            # -----------------------
            # TYPE
            # -----------------------
            elif action == "type":

                type_text(step["text"])


            # -----------------------
            # PRESS
            # -----------------------
            elif action == "press":

                press(step["key"])


            # -----------------------
            # HOTKEY
            # -----------------------
            elif action == "hotkey":

                hotkey(*step["keys"])


            # -----------------------
            # CLICK
            # -----------------------
            elif action == "click":

                click()


            # -----------------------
            # FOCUS WINDOW
            # -----------------------
            elif action == "focus":

                focus_window(step["title"])

                wait(1)


            # -----------------------
            # CREATE FILE
            # -----------------------
            elif action == "create_file":

                create_file(step["path"])


            # -----------------------
            # TERMINAL
            # -----------------------
            elif action == "terminal":

                run_terminal_command(step["cmd"])


            else:
                print("Unknown action:", action)


        except Exception as e:
            print("Workflow error:", e)