from execution.executor import execute_plan


plan = {
    "workflow": [

        {"action": "open_app", "name": "notepad"},
        {"action": "wait", "time": 2},

        {"action": "type", "text": "Fury Step 24 working"},
        {"action": "press", "key": "enter"},

        {"action": "type", "text": "Workflow engine ok"}
    ]
}


execute_plan(plan)