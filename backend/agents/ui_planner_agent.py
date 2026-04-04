from agents.base_agent import BaseAgent


class UIPlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("UIPlannerAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "ui_goal"

    def handle(self, task):

        goal = task.get("goal", "")
        platform = task.get("platform")

        print("UIPlannerAgent → planning:", goal, "on", platform)

        # =========================
        # 🔥 YOUTUBE SEARCH (FINAL STABLE VERSION)
        # =========================

        if platform == "youtube" and "search" in goal:

            query = goal.replace("search", "").strip()

            return {
                "intent": "ui_action_sequence",
                "data": [

                    # 1. open YouTube
                    {"action": "open_url", "url": "https://www.youtube.com"},

                    # 2. wait for page
                    {"action": "wait", "time": 3},

                    # 3. try shortcut focus
                    {"action": "press", "key": "/"},

                    {"action": "wait", "time": 1},

                    # 🔥 fallback click (important)
                    {"action": "click", "x": 900, "y": 120},

                    {"action": "wait", "time": 1},

                    # 4. type query
                    {"action": "type", "text": query},

                    # 5. enter
                    {"action": "press", "key": "enter"}
                ]
            }

        return None