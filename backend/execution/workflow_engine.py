# import time

# from automation.ui_engine import type_text, press, hotkey, wait, click
# from automation.software_control import open_application
# from automation.window_manager import focus_window
# from automation.file_manager import create_file

# from developer.terminal_engine import run_terminal_command
# from browser.browser_agent import open_website

# from brain.context_memory import memory
# from skills.skill_manager import execute_skill


# MAX_STEP_RETRY = 2


# def run_workflow(steps):

#     if not steps:
#         print("No workflow steps")
#         return

#     print("Running workflow...")

#     for step in steps:

#         retry = 0

#         while retry <= MAX_STEP_RETRY:

#             try:

#                 action = step.get("action")

#                 print("STEP:", step)

#                 # -----------------------
#                 # OPEN APP
#                 # -----------------------
#                 if action == "open_app":

#                     name = step["name"]

#                     open_application(name)

#                     wait(3)

#                     focus_window(name)

#                     memory.set_app(name)
#                     memory.set_window(name)
#                     memory.set_action("open_app")

#                     break

#                 # -----------------------
#                 # OPEN URL (🔥 FINAL FIX)
#                 # -----------------------
#                 elif action == "open_url":

#                     url = step["url"]

#                     open_website(url)

#                     wait(4)

#                     # 🔥 STRONG FOCUS
#                     focus_window("chrome")

#                     # 🔥 FORCE CORRECT TAB
#                     hotkey("ctrl", "l")
#                     wait(0.5)
#                     press("esc")
#                     wait(0.3)

#                     # 🔥 CONTEXT SET
#                     if "youtube" in url:
#                         memory.set_site("youtube")
#                     elif "google" in url:
#                         memory.set_site("google")
#                     else:
#                         memory.set_site(url)

#                     memory.set_app("browser")
#                     memory.set_window("chrome")
#                     memory.set_action("open_website")

#                     break

#                 # -----------------------
#                 # WAIT
#                 # -----------------------
#                 elif action == "wait":

#                     wait(step.get("time", 1))
#                     break

#                 # -----------------------
#                 # TYPE (🔥 CLEAN)
#                 # -----------------------
#                 elif action == "type":

#                     app = memory.get_app()

#                     if app == "browser":
#                         focus_window("chrome")
#                         wait(0.5)

#                     else:
#                         win = memory.get_window()
#                         if win:
#                             focus_window(win)
#                             wait(0.5)

#                     print("Typing:", step["text"])

#                     type_text(step["text"])

#                     memory.set_action("type_text")

#                     break

#                 # -----------------------
#                 # PRESS
#                 # -----------------------
#                 elif action == "press":

#                     press(step["key"])
#                     break

#                 # -----------------------
#                 # HOTKEY
#                 # -----------------------
#                 elif action == "hotkey":

#                     hotkey(*step["keys"])
#                     break

#                 # -----------------------
#                 # CLICK
#                 # -----------------------
#                 elif action == "click":

#                     click()
#                     break

#                 # -----------------------
#                 # CREATE FILE
#                 # -----------------------
#                 elif action == "create_file":

#                     path = step["path"]

#                     create_file(path)

#                     memory.set_file(path)
#                     memory.set_action("create_file")

#                     break

#                 # -----------------------
#                 # TERMINAL
#                 # -----------------------
#                 elif action == "terminal":

#                     run_terminal_command(step["cmd"])

#                     memory.set_action("run_terminal")

#                     break

#                 # -----------------------
#                 # SKILL (SAFE)
#                 # -----------------------
#                 elif action == "skill":

#                     task = step.get("data")

#                     # 🔥 PREVENT DUPLICATE WEBSITE OPEN
#                     if task.get("intent") == "open_website":
#                         print("Skipping duplicate open_website skill")
#                         break

#                     if task:

#                         ok = execute_skill(task)

#                         if ok:
#                             break

#                     raise Exception("Skill failed")

#                 else:

#                     raise Exception("Unknown action")

#             except Exception as e:

#                 retry += 1

#                 print("Step error:", e, "Retry:", retry)

#                 if retry > MAX_STEP_RETRY:
#                     print("Skipping step")
#                     break



import time

from automation.ui_engine import type_text, press, hotkey, wait, click
from automation.software_control import open_application
from automation.window_manager import focus_window
from automation.file_manager import create_file

from developer.terminal_engine import run_terminal_command
from browser.browser_agent import open_website

from brain.context_memory import memory
from brain.failure_memory import save_failure      # ✅ STEP 108
from skills.skill_manager import execute_skill


MAX_STEP_RETRY = 2


def run_workflow(steps):

    if not steps:
        print("No workflow steps")
        return

    print("Running workflow...")

    for step in steps:

        retry = 0

        while retry <= MAX_STEP_RETRY:

            try:

                action = step.get("action")

                print("STEP:", step)

                if action == "open_app":

                    name = step["name"]
                    open_application(name)
                    wait(3)
                    focus_window(name)
                    memory.set_app(name)
                    memory.set_window(name)
                    memory.set_action("open_app")
                    break

                elif action == "open_url":

                    url = step["url"]
                    open_website(url)
                    wait(3)
                    focus_window("chrome")
                    hotkey("ctrl", "l")
                    wait(0.3)
                    press("esc")
                    wait(0.3)

                    if "youtube" in url:
                        memory.set_site("youtube")
                    elif "google" in url:
                        memory.set_site("google")
                    else:
                        memory.set_site(url)

                    memory.set_app("browser")
                    memory.set_window("chrome")
                    memory.set_action("open_website")
                    break

                elif action == "wait":

                    wait(step.get("time", 1))
                    break

                elif action == "type":

                    app = memory.get_app()

                    if app == "browser":
                        focus_window("chrome")
                        wait(0.5)
                    else:
                        win = memory.get_window()
                        if win:
                            focus_window(win)
                            wait(0.5)

                    print("Typing:", step["text"])
                    type_text(step["text"])
                    memory.set_action("type_text")
                    break

                elif action == "press":

                    press(step["key"])
                    break

                elif action == "hotkey":

                    hotkey(*step["keys"])
                    break

                elif action == "click":

                    click()
                    break

                elif action == "create_file":

                    path = step["path"]
                    create_file(path)
                    memory.set_file(path)
                    memory.set_action("create_file")
                    break

                elif action == "terminal":

                    run_terminal_command(step["cmd"])
                    memory.set_action("run_terminal")
                    break

                elif action == "skill":

                    task = step.get("data")

                    if task and task.get("intent") == "open_website":
                        print("Skipping duplicate open_website skill")
                        break

                    if task:
                        ok = execute_skill(task)
                        if ok:
                            break

                    raise Exception("Skill failed")

                else:
                    raise Exception("Unknown action: " + str(action))

            except Exception as e:

                # ✅ STEP 108 — learn from failure
                save_failure(step, e)

                retry += 1
                print("Step error:", e, "Retry:", retry)

                if retry > MAX_STEP_RETRY:
                    print("Skipping step")
                    break