# planner/graph_planner.py


class TaskNode:

    def __init__(self, action, data=None):

        self.action = action
        self.data = data or {}
        self.next = []


class GraphPlan:

    def __init__(self):

        self.nodes = []

    def add(self, node):

        self.nodes.append(node)

    def run(self, controller):

        for n in self.nodes:

            task = {
                "action": n.action,
                **n.data,
            }

            controller.execute(task)


def build_graph_plan(tasks):

    plan = GraphPlan()

    for t in tasks:

        node = TaskNode(
            action=t.get("action") or t.get("intent"),
            data=t,
        )

        plan.add(node)

    return plan