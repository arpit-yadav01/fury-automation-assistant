# execution/auto_mode_v2.py

from agents.agent_controller import controller

from planner.graph_planner import build_graph_plan

from agents.observer_agent import ObserverAgent

from brain.context_memory import memory


MAX_AUTO_STEPS = 15


observer = ObserverAgent()


def run_auto_v2(tasks):

    print("AUTO MODE V2")

    plan = build_graph_plan(tasks)

    step = 0

    last_action = None

    while step < MAX_AUTO_STEPS:

        print("AUTO STEP", step + 1)

        for node in plan.nodes:

            controller.execute(
                {
                    "action": node.action,
                    **node.data,
                }
            )

            obs = observer.handle(
                {
                    "observe": True
                }
            )

            action = memory.get_action()

            if action == last_action:
                print("No change")
                return

            last_action = action

        step += 1

    print("AUTO FINISHED")