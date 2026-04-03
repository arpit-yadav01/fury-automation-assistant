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
        # ✅ YOUTUBE SEARCH (FINAL FIX)
        # =========================

        if platform == "youtube" and "search" in goal:

            query = goal.replace("search", "").strip()

            return {
                "intent": "ui_action_sequence",
                "data": [

                    # STEP 1 → open YouTube
                    {
                        "action": "open_url",
                        "url": "https://www.youtube.com"
                    },

                    # STEP 2 → wait for load
                    {
                        "action": "wait",
                        "time": 3
                    },

                    # STEP 3 → focus search bar (shortcut)
                    {
                        "action": "press",
                        "key": "/"
                    },

                    # STEP 4 → type query
                    {
                        "action": "type",
                        "text": query
                    },

                    # STEP 5 → press enter
                    {
                        "action": "enter"
                    }
                ]
            }

        return None