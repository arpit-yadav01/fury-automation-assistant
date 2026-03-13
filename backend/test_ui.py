from automation.ui_engine import *

print("Starting UI test in 2 seconds...")
wait(2)

print("Move")
move(500, 500)

print("Click")
click()

print("Typing")
type_text("Fury UI Engine Working")

press("enter")

type_text("Done")