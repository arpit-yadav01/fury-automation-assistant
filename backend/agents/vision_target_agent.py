from agents.base_agent import BaseAgent
from vision.object_detector import detect_ui_objects


class VisionTargetAgent(BaseAgent):

    def __init__(self):
        super().__init__("VisionTargetAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "detect_ui"

    def handle(self, task):

        print("VisionTargetAgent → detecting UI objects")

        objects = detect_ui_objects()

        print("Detected objects:", len(objects))

        return {
            "intent": "ui_objects",
            "data": objects
        }