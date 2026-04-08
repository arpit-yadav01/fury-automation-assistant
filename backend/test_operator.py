from automation.ui_click_engine import safe_click
from automation.ui_action_engine import perform_ui_action
from execution.operator_loop import run_operator_loop


print("\n--- TEST 1: CLICK ---")
safe_click(x=500, y=500)


print("\n--- TEST 2: ACTION ---")
perform_ui_action({
    "action": "click",
    "x": 500,
    "y": 500
})


print("\n--- TEST 3: LOOP ---")
actions = [
    {"action": "click", "x": 500, "y": 500},
    {"action": "type", "text": "hello fury"},
    {"action": "enter"}
]

run_operator_loop(actions)


