# agents/browser_agent.py

from agents.base_agent import BaseAgent

from browser.browser_agent import (
    open_website,
    search_on_page,
)


class BrowserAgent(BaseAgent):

    def __init__(self):
        super().__init__("BrowserAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        action = task.get("action")
        intent = task.get("intent")

        if action == "open_url":
            return True

        if intent in ["open_website", "web_search"]:
            return True

        return False

    # -------------------------

    def handle(self, task):

        action = task.get("action")
        intent = task.get("intent")

        # workflow action

        if action == "open_url":

            url = task.get("url")

            open_website(url)

            return

        # intent

        if intent == "open_website":

            url = task.get("url")

            open_website(url)

            return

        if intent == "web_search":

            query = task.get("query")
            site = task.get("site", "google")

            if site == "youtube":
                open_website("https://youtube.com")
                search_on_page(query)
            else:
                open_website(
                    f"https://www.google.com/search?q={query}"
                )

            return