# execution/workflow_engine.py

import time

from automation.ui_engine import type_text, press, hotkey, wait, click
from automation.software_control import open_application
from automation.window_manager import focus_window
from automation.file_manager import create_file

from developer.terminal_engine import run_terminal_command
from browser.browser_agent import open_website

from brain.context_memory import memory


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

                wait(3)

                focus_window(name)

                wait(1)

                memory.set_app(name)
                memory.set_window(name)
                memory.set_action("open_app")


            # -----------------------
            # OPEN URL
            # -----------------------
            elif action == "open_url":

                url = step["url"]

                open_website(url)

                wait(4)

                focus_window("chrome")

                wait(1)

                memory.set_site(url)
                memory.set_app("browser")
                memory.set_window("chrome")
                memory.set_action("open_website")


            # -----------------------
            # WAIT
            # -----------------------
            elif action == "wait":

                wait(step.get("time", 1))


            # -----------------------
            # TYPE
            # -----------------------
            elif action == "type":

                app = memory.get_app()

                # ------------------
                # BROWSER
                # ------------------
                if app == "browser":

                    focus_window("chrome")
                    wait(1)

                    print("Browser detected, trying vision click")

                    clicked = False

                    try:
                        from vision.ui_click import click_text_safe

                        # try multiple labels
                        for label in [
                            "Search",
                            "search",
                            "Search YouTube",
                            "YouTube",
                            "Search Google"
                        ]:

                            if click_text_safe(label, retries=2):
                                clicked = True
                                break

                    except Exception as e:
                        print("Vision error:", e)

                    if not clicked:
                        print("Vision failed → fallback click")
                        click()
                        wait(1)

                # ------------------
                # NORMAL APP
                # ------------------
                else:

                    win = memory.get_window()

                    if win:
                        focus_window(win)
                        wait(1)

                type_text(step["text"])

                memory.set_action("type_text")


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

                path = step["path"]

                create_file(path)

                memory.set_file(path)
                memory.set_action("create_file")


            # -----------------------
            # TERMINAL
            # -----------------------
            elif action == "terminal":

                run_terminal_command(step["cmd"])

                memory.set_action("run_terminal")


            else:
                print("Unknown action:", action)


        except Exception as e:
            print("Workflow error:", e)