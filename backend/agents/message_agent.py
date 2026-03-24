# agents/message_agent.py

from agents.base_agent import BaseAgent

from core.message_bus import bus


class MessageAgent(BaseAgent):

    def __init__(self):
        super().__init__("MessageAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("message"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        data = task.get("message")

        sender = data.get("from", "unknown")
        target = data.get("to", "all")

        bus.send(sender, target, data)

        print("Message sent")

        return