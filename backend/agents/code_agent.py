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