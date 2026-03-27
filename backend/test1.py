import os
from openai import OpenAI


GROQ_KEY = os.getenv("GROQ_API_KEY")

client = None

if GROQ_KEY:

    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )


def generate_code(language, task):

    if client is None:
        print("No LLM key")
        return ""

    try:

        prompt = f"""
Write {language} code for:

{task}

Return only code.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You write only code"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        text = response.choices[0].message.content

        if not text:
            return ""

        return text.strip()

    except Exception as e:

        print("Code gen error:", e)
        return ""
    
    # developer/terminal_engine.py

import subprocess


def run_terminal_command(command):

    try:

        print(f"Running command: {command}")

        subprocess.run(command, shell=True)

    except Exception as e:

        print("Terminal command failed:", e)


        # # agents/code_agent.py

# from agents.base_agent import BaseAgent

# from developer.code_generator import generate_code


# class CodeAgent(BaseAgent):

#     def __init__(self):
#         super().__init__("CodeAgent")

#     # -------------------------

#     def can_handle(self, task):

#         if not isinstance(task, dict):
#             return False

#         if task.get("intent") == "generate_code":
#             return True

#         return False

#     # -------------------------

#     def handle(self, task):

#         lang = task.get("language", "python")
#         t = task.get("task", "")

#         print("CodeAgent generating code")

#         code = generate_code(lang, t)

#         print(code)

#         return code


from agents.base_agent import BaseAgent
from developer.code_generator import generate_code

from brain.context_memory import memory
from automation.file_manager import write_to_file


class CodeAgent(BaseAgent):

    def __init__(self):
        super().__init__("CodeAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("intent") == "generate_code":
            return True

        return False

    def handle(self, task):

        lang = task.get("language", "python")
        t = task.get("task", "")

        print("CodeAgent generating code")

        code = generate_code(lang, t)

        if not code:
            print("No code generated")
            return

        # ✅ FIX — remove ```python ```
        code = code.strip()

        if code.startswith("```"):
            code = code.replace("```python", "")
            code = code.replace("```", "")
            code = code.strip()

        print(code)

        # write to last file
        file = memory.get_file()

        if file:
            write_to_file(file, code)
            print("Written to", file)
        else:
            print("No file in memory, only printing")


        
        from agents.base_agent import BaseAgent

from developer.dev_workflow import (
    open_vscode,
    create_new_file,
    write_code,
    save_file,
    run_python_file,
    run_command,
)


class DevAgent(BaseAgent):

    def __init__(self):
        super().__init__("DevAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("dev"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        cmd = task.get("dev")

        if cmd == "open_vscode":
            open_vscode()
            return

        if cmd == "new_file":
            create_new_file(task.get("name", "test.py"))
            return

        if cmd == "write":
            write_code(task.get("code", ""))
            return

        if cmd == "save":
            save_file()
            return

        if cmd == "run":
            run_python_file(task.get("name", "test.py"))
            return

        if cmd == "command":
            run_command(task.get("cmd", ""))
            return
        
        # agents/error_analyzer_agent.py

from agents.base_agent import BaseAgent

from core.message_bus import bus


class ErrorAnalyzerAgent(BaseAgent):

    def __init__(self):
        super().__init__("ErrorAnalyzerAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("error"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        print("ErrorAnalyzerAgent")

        error = task.get("error")
        last = task.get("last_task")

        print("Error:", error)

        decision = {
            "retry": False,
            "skip": False,
            "replan": False,
        }

        # simple logic

        if "not found" in str(error).lower():
            decision["retry"] = True

        elif "timeout" in str(error).lower():
            decision["retry"] = True

        else:
            decision["replan"] = True

        bus.send(
            "ErrorAnalyzer",
            "controller",
            decision,
        )

        return decision
    
    execution/error_solver.py (if exists) no such file 