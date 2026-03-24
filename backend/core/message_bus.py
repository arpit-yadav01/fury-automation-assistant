# core/message_bus.py


class MessageBus:

    def __init__(self):

        self.messages = []

    # ---------------------

    def send(self, sender, target, data):

        msg = {
            "from": sender,
            "to": target,
            "data": data,
        }

        self.messages.append(msg)

    # ---------------------

    def get(self, target):

        out = []

        for m in self.messages:

            if m["to"] == target or m["to"] == "all":
                out.append(m)

        return out

    # ---------------------

    def clear(self):

        self.messages = []


bus = MessageBus()