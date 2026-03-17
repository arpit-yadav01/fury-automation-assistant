from execution.executor import execute_plan


plan = [

    {"intent": "open_app", "app": "notepad"},

    {"intent": "type_text", "text": "normal typing"},

]

execute_plan(plan)