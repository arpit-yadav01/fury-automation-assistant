# agents/screen_memory_agent.py

from agents.base_agent import BaseAgent
from vision.layout_detector import detect_layout
from memory.screen_memory import store_elements


class ScreenMemoryAgent(BaseAgent):

    def __init__(self):
        super().__init__("ScreenMemoryAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "capture_screen"

    def handle(self, task):

        print("ScreenMemoryAgent → capturing screen")

        elements = detect_layout(debug=True)

        store_elements(elements)

        print("Stored elements:", len(elements))

        return elements