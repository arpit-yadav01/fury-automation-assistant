from execution.executor import execute_plan
from brain.context_memory import memory


plan = [

    {"intent": "open_app", "app": "notepad"},
    {"intent": "type_text", "text": "hello"},
]

execute_plan(plan)

print("APP:", memory.get_app())
print("WINDOW:", memory.get_window())
print("ACTION:", memory.get_action())