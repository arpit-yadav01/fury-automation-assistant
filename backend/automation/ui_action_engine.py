from vision.ui_click import click_text
from automation.typing_engine import type_text
from automation.ui_engine import press


def perform_ui_action(action):

    if not isinstance(action, dict):
        print("Invalid UI action")
        return None

    act = action.get("action")

    # -----------------------
    # CLICK TEXT
    # -----------------------

    if act == "click_text":

        text = action.get("text")

        if text:
            print("Clicking text:", text)
            return click_text(text)

    # -----------------------
    # TYPE TEXT
    # -----------------------

    if act == "type":

        text = action.get("text")

        if text:
            print("Typing:", text)
            return type_text(text)

    # -----------------------
    # PRESS ENTER
    # -----------------------

    if act == "enter":

        print("Pressing Enter")
        return press("enter")

    # -----------------------

    print("Unknown UI action:", action)

    return None