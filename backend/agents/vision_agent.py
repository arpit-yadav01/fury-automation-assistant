# agents/vision_agent.py

from agents.base_agent import BaseAgent

from vision.screen_capture import capture_screen
from vision.text_detection import find_text_on_screen

from vision.ui_click import click_text


class VisionAgent(BaseAgent):

    def __init__(self):
        super().__init__("VisionAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("vision"):
            return True

        if task.get("find_text"):
            return True

        if task.get("click_text"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        # capture screen

        if task.get("vision") == "capture":

            print("VisionAgent → capture")

            img = capture_screen()

            return img

        # find text

        if task.get("find_text"):

            text = task.get("find_text")

            pos = find_text_on_screen(text)

            print("Found:", pos)

            return pos

        # click text

        if task.get("click_text"):

            text = task.get("click_text")

            click_text(text)

            return