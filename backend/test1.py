# brain/context_memory.py


class ContextMemory:

    def __init__(self):

        self.current_app = None
        self.current_window = None
        self.last_site = None
        self.last_file = None
        self.last_action = None

    # ---------------------

    def set_app(self, app):

        print("Memory app:", app)

        self.current_app = app

    # ---------------------

    def set_window(self, window):

        print("Memory window:", window)

        self.current_window = window

    # ---------------------

    def set_site(self, site):

        print("Memory site:", site)

        self.last_site = site

    # ---------------------

    def set_file(self, file):

        print("Memory file:", file)

        self.last_file = file

    # ---------------------

    def set_action(self, action):

        self.last_action = action

    # ---------------------

    def get_app(self):
        return self.current_app

    def get_window(self):
        return self.current_window

    def get_site(self):
        return self.last_site

    def get_file(self):
        return self.last_file

    def get_action(self):
        return self.last_action


# global memory

memory = ContextMemory()

# agents/context_agent.py

from agents.base_agent import BaseAgent

from automation.window_manager import (
    get_active_window_title,
)

from brain.context_memory import memory


class ContextTrackingAgent(BaseAgent):

    def __init__(self):
        super().__init__("ContextTrackingAgent")

    # -------------------------

    def can_handle(self, task):

        if isinstance(task, dict) and task.get("context_check"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        title = get_active_window_title()

        if not title:
            return

        title_low = title.lower()

        print("ContextAgent →", title)

        memory.set_window(title)

        if "chrome" in title_low:
            memory.set_app("browser")

        elif "code" in title_low:
            memory.set_app("vscode")

        elif "notepad" in title_low:
            memory.set_app("notepad")

        elif "cmd" in title_low or "powershell" in title_low:
            memory.set_app("terminal")

        else:
            memory.set_app(title_low)

        
        # brain/ai_interpreter.py

def clean_query(text):

    words_to_remove = [
        "open",
        "and",
        "youtube",
        "google",
        "search",
        "for",
    ]

    for w in words_to_remove:
        text = text.replace(w, "")

    return text.strip()


def interpret_command(command):

    command = command.lower().strip()

    # -------------------------
    # YOUTUBE SEARCH
    # -------------------------

    if "youtube" in command and "search" in command:

        query = clean_query(command)

        return {
            "intent": "web_search",
            "site": "youtube",
            "query": query
        }

    # -------------------------
    # GOOGLE SEARCH
    # -------------------------

    if "google" in command or command.startswith("search"):

        query = clean_query(command)

        return {
            "intent": "web_search",
            "site": "google",
            "query": query
        }

    return None


import re
import os
from openai import OpenAI

GROQ_KEY = os.getenv("GROQ_API_KEY")

client = None

if GROQ_KEY:
    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )


def interpret_with_llm(command):

    if client is None:
        return None

    try:

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "Return ONLY JSON list of tasks"
                },
                {
                    "role": "user",
                    "content": command
                }
            ]
        )

        text = response.choices[0].message.content.strip()

        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)

        return json.loads(text)

    except Exception:
        return None