# developer/dev_workflow.py

from automation.software_control import open_application
from automation.window_manager import focus_window
from automation.ui_engine import type_text, press, hotkey, wait
from developer.terminal_engine import run_terminal_command


# -----------------------
# OPEN VSCODE
# -----------------------

def open_vscode():

    print("Opening VS Code")

    open_application("vscode")

    wait(2)

    focus_window("Code")


# -----------------------
# CREATE NEW FILE
# -----------------------

def create_new_file(filename):

    print("Creating new file:", filename)

    hotkey("ctrl", "n")

    wait(1)

    hotkey("ctrl", "s")

    wait(1)

    type_text(filename)

    press("enter")

    wait(1)


# -----------------------
# WRITE CODE
# -----------------------

def write_code(code):

    print("Writing code")

    type_text(code)


# -----------------------
# SAVE FILE
# -----------------------

def save_file():

    hotkey("ctrl", "s")

    wait(1)


# -----------------------
# RUN PYTHON FILE
# -----------------------

def run_python_file(filename):

    print("Running python file")

    hotkey("ctrl", "`")

    wait(1)

    run_terminal_command(f"python {filename}")


# -----------------------
# RUN TERMINAL COMMAND
# -----------------------

def run_command(cmd):

    print("Running command:", cmd)

    hotkey("ctrl", "`")

    wait(1)

    run_terminal_command(cmd)