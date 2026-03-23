# agents/jarvis_controller.py

from agents.agent_controller import controller

from execution.task_planner import create_plan

from brain.context_memory import memory


MAX_JARVIS_STEPS = 10


class JarvisController:

    def __init__(self):
        self.running = False

    # -------------------------

    def run_once(self, command):

        plan = create_plan(command)

        if not plan:
            print("No plan")
            return

        controller.execute(plan)

    # -------------------------

    def run_loop(self, command):

        print("Jarvis loop started")

        step = 0

        last_action = None

        while step < MAX_JARVIS_STEPS:

            print("\nJARVIS STEP", step + 1)

            plan = create_plan(command)

            if not plan:
                print("No plan")
                break

            controller.execute(plan)

            action = memory.get_action()

            if action == last_action:
                print("No change, stopping")
                break

            last_action = action

            step += 1

        print("Jarvis loop finished")


jarvis = JarvisController()