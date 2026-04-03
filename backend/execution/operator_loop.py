from automation.ui_action_engine import perform_ui_action

MAX_STEPS = 10


def run_operator_loop(actions):

    print("OperatorLoop → started")

    if not actions:
        print("No actions")
        return

    step = 0

    for action in actions:

        if step >= MAX_STEPS:
            print("Max steps reached")
            break

        print("\nSTEP", step + 1, "→", action)

        success = perform_ui_action(action)

        if not success:
            print("Step failed, stopping loop")
            break

        step += 1

    print("OperatorLoop → finished")