from automation.ui_engine import *
from automation.window_manager import *

print("Active:", get_active_window_title())

wait(2)

type_text("Fury step 23 test")

press("enter")

print("Windows:", list_windows())