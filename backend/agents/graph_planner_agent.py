# agents/graph_planner_agent.py

from agents.base_agent import BaseAgent

from planner.graph_planner import build_graph_plan


class GraphPlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("GraphPlannerAgent")

    # ---------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("graph_plan"):
            return True

        return False

    # ---------------------

    def handle(self, task):

        tasks = task.get("tasks")

        plan = build_graph_plan(tasks)

        return plan