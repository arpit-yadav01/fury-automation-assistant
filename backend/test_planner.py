from execution.executor import execute_plan
from execution.task_planner import create_plan

cmd = "open notepad and type hello"

plan = create_plan(cmd)

print(plan)

execute_plan(plan)