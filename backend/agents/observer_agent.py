# agents/observer_agent.py

from agents.base_agent import BaseAgent

from automation.window_manager import get_active_window_title
from vision.text_detection import find_text_on_screen

from brain.context_memory import memory


class ObserverAgent(BaseAgent):

    def __init__(self):
        super().__init__("ObserverAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("observe"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        print("ObserverAgent")

        window = get_active_window_title()

        last_action = memory.get_action()

        result = {
            "window": window,
            "action": last_action,
        }

        text = task.get("check_text")

        if text:

            pos = find_text_on_screen(text)

            result["text_found"] = pos is not None

        print("OBS:", result)

        return result