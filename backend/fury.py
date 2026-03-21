# from execution.task_planner import create_plan
# from execution.executor import execute_plan
# from execution.auto_loop import run_autonomous
# from execution.goal_engine import run_goal

# from brain.context_memory import memory

# from voice.speech_to_text import listen_once
# from voice.text_to_speech import speak


# voice_mode = False
# jarvis_mode = False


# # -----------------------------
# # PRINT MEMORY
# # -----------------------------

# def show_memory():

#     print("---- MEMORY ----")

#     print("App:", memory.get_app())
#     print("Window:", memory.get_window())
#     print("Site:", memory.get_site())
#     print("File:", memory.get_file())
#     print("Action:", memory.get_action())

#     print("----------------")


# # -----------------------------
# # GET COMMAND
# # -----------------------------

# def get_command():

#     global voice_mode, jarvis_mode

#     if jarvis_mode:
#         text = listen_once()
#         return text if text else ""

#     if voice_mode:
#         text = listen_once()
#         return text if text else ""

#     return input(">>> ").strip()


# # -----------------------------
# # MAIN LOOP
# # -----------------------------

# def start_fury():

#     global voice_mode, jarvis_mode

#     print("=================================")
#     print("🔥 FURY AI ASSISTANT STARTED")
#     print("voice mode / jarvis mode / exit")
#     print("=================================")

#     while True:

#         command = get_command()

#         if not command:
#             continue

#         cmd = command.lower()


#         # -------------------------
#         # EXIT
#         # -------------------------

#         if cmd == "exit":

#             speak("Shutting down")

#             print("Shutting down Fury")

#             break


#         # -------------------------
#         # VOICE MODE
#         # -------------------------

#         if cmd == "voice mode":

#             voice_mode = True
#             jarvis_mode = False

#             speak("Voice mode activated")

#             continue


#         if cmd == "text mode":

#             voice_mode = False
#             jarvis_mode = False

#             speak("Text mode")

#             continue


#         # -------------------------
#         # JARVIS MODE
#         # -------------------------

#         if cmd == "jarvis mode":

#             jarvis_mode = True
#             voice_mode = False

#             speak("Jarvis mode activated")

#             continue


#         if cmd == "stop jarvis":

#             jarvis_mode = False

#             speak("Jarvis stopped")

#             continue


#         # -------------------------
#         # GOAL MODE
#         # -------------------------

#         if command.startswith("goal "):

#             goal = command.replace("goal ", "")

#             speak("Goal mode")

#             run_goal(goal)

#             continue


#         # -------------------------
#         # AUTO MODE
#         # -------------------------

#         if command.startswith("auto "):

#             goal = command.replace("auto ", "")

#             speak("Autonomous mode")

#             run_autonomous(goal)

#             continue


#         # -------------------------
#         # NORMAL EXECUTION
#         # -------------------------

#         plan = create_plan(command)

#         print("\nExecution Plan:")

#         if isinstance(plan, dict):
#             print(plan)
#         else:
#             for step in plan:
#                 print(step)

#         speak("Executing")

#         execute_plan(plan)

#         speak("Done")

#         show_memory()


# # -----------------------------

# if __name__ == "__main__":
#     start_fury()









from execution.task_planner import create_plan
from execution.executor import execute_plan
from execution.auto_loop import run_autonomous
from execution.goal_engine import run_goal

from brain.context_memory import memory

from voice.speech_to_text import listen_once
from voice.text_to_speech import speak


# ✅ STEP 42 IMPORTS
from agents.register_agents import register_all_agents
from agents.agent_controller import controller


voice_mode = False
jarvis_mode = False


# -----------------------------
# PRINT MEMORY
# -----------------------------

def show_memory():

    print("---- MEMORY ----")

    print("App:", memory.get_app())
    print("Window:", memory.get_window())
    print("Site:", memory.get_site())
    print("File:", memory.get_file())
    print("Action:", memory.get_action())

    print("----------------")


# -----------------------------
# GET COMMAND
# -----------------------------

def get_command():

    global voice_mode, jarvis_mode

    if jarvis_mode:
        text = listen_once()
        return text if text else ""

    if voice_mode:
        text = listen_once()
        return text if text else ""

    return input(">>> ").strip()


# -----------------------------
# MAIN LOOP
# -----------------------------

def start_fury():

    global voice_mode, jarvis_mode

    print("=================================")
    print("🔥 FURY AI ASSISTANT STARTED")
    print("voice mode / jarvis mode / exit")
    print("=================================")

    # ✅ STEP 42 REGISTER AGENTS
    register_all_agents()

    while True:

        command = get_command()

        if not command:
            continue

        cmd = command.lower()


        # -------------------------
        # EXIT
        # -------------------------

        if cmd == "exit":

            speak("Shutting down")

            print("Shutting down Fury")

            break


        # -------------------------
        # VOICE MODE
        # -------------------------

        if cmd == "voice mode":

            voice_mode = True
            jarvis_mode = False

            speak("Voice mode activated")

            continue


        if cmd == "text mode":

            voice_mode = False
            jarvis_mode = False

            speak("Text mode")

            continue


        # -------------------------
        # JARVIS MODE
        # -------------------------

        if cmd == "jarvis mode":

            jarvis_mode = True
            voice_mode = False

            speak("Jarvis mode activated")

            continue


        if cmd == "stop jarvis":

            jarvis_mode = False

            speak("Jarvis stopped")

            continue


        # -------------------------
        # GOAL MODE
        # -------------------------

        if command.startswith("goal "):

            goal = command.replace("goal ", "")

            speak("Goal mode")

            run_goal(goal)

            continue


        # -------------------------
        # AUTO MODE
        # -------------------------

        if command.startswith("auto "):

            goal = command.replace("auto ", "")

            speak("Autonomous mode")

            run_autonomous(goal)

            continue


        # -------------------------
        # NORMAL EXECUTION
        # -------------------------

        plan = create_plan(command)

        print("\nExecution Plan:")

        if isinstance(plan, dict):
            print(plan)
        else:
            for step in plan:
                print(step)

        speak("Executing")

        # ✅ STEP 42 CHANGE
        controller.execute(plan)

        speak("Done")

        show_memory()


# -----------------------------

if __name__ == "__main__":
    start_fury()
