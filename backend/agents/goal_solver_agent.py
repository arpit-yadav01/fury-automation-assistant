from agents.base_agent import BaseAgent


class GoalSolverAgent(BaseAgent):

    def __init__(self):
        super().__init__("GoalSolverAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        # ✅ prevent re-loop
        if task.get("forwarded"):
            return False

        return task.get("intent") == "goal_task"

    def handle(self, task):

        data = task.get("data", {})

        goal = data.get("goal")
        typ = data.get("type")

        print("GoalSolverAgent → solving:", goal, typ)

        # ✅ PASS FORWARD (do not stop pipeline)
        return {
            "intent": "goal_task",
            "data": data,
            "raw": task.get("raw"),
            "forwarded": True   # prevents re-handling
        }