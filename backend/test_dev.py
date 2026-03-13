from execution.executor import execute_plan


plan = [

    {"intent": "open_vscode"},

    {"intent": "create_code_file", "filename": "hello.py"},

    {
        "intent": "write_code",
        "code": 'print("Hello from Fury")'
    },

    {"intent": "save_file"},

]


execute_plan(plan)