from agents.base_agent import BaseAgent
from vision.layout_detector import detect_layout
from vision.ui_graph import build_ui_graph


class UILayoutAgent(BaseAgent):

    def __init__(self):
        super().__init__("UILayoutAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "analyze_ui"

    def handle(self, task):

        print("UILayoutAgent → analyzing UI")

        elements = detect_layout()

        graph = build_ui_graph(elements)

        print("UI Elements:", len(graph))

        return {
            "intent": "ui_graph",
            "data": graph
        }