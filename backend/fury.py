
# from dotenv import load_dotenv
# load_dotenv()
# from execution.task_planner import create_plan
# from execution.auto_loop import run_autonomous

# from brain.context_memory import memory

# from voice.speech_to_text import listen_once
# from voice.text_to_speech import speak

# # AGENTS
# from agents.register_agents import register_all_agents
# from agents.agent_controller import controller
# from agents.jarvis_controller import jarvis

# # FIX-1 FinalCore
# from core.final_core import final_core


# voice_mode = False
# jarvis_mode = False


# def show_memory():

#     print("---- MEMORY ----")

#     print("App:", memory.get_app())
#     print("Window:", memory.get_window())
#     print("Site:", memory.get_site())
#     print("File:", memory.get_file())
#     print("Action:", memory.get_action())

#     print("----------------")


# def get_command():

#     global voice_mode, jarvis_mode

#     if jarvis_mode:
#         text = listen_once()
#         return text if text else ""

#     if voice_mode:
#         text = listen_once()
#         return text if text else ""

#     return input(">>> ").strip()


# def start_fury():

#     global voice_mode, jarvis_mode

#     print("=================================")
#     print("🔥 FURY AI ASSISTANT STARTED")
#     print("voice mode / jarvis mode / exit")
#     print("=================================")

#     register_all_agents()

#     while True:

#         command = get_command()

#         if not command:
#             continue

#         cmd = command.lower()

#         if cmd == "exit":
#             speak("Shutting down")
#             print("Shutting down Fury")
#             break

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

#         if cmd == "jarvis mode":

#             jarvis_mode = True
#             voice_mode = False

#             speak("Jarvis mode activated")

#             while jarvis_mode:

#                 text = listen_once()

#                 if not text:
#                     continue

#                 if text == "stop jarvis":
#                     jarvis_mode = False
#                     break

#                 jarvis.run_loop(text)

#             continue

#         if command.startswith("goal "):

#             goal = command.replace("goal ", "")

#             speak("Goal mode")

#             jarvis.run_loop(goal)

#             continue

#         if command.startswith("auto "):

#             goal = command.replace("auto ", "")

#             speak("Autonomous mode")

#             run_autonomous(goal)

#             continue

#         # ---------- NORMAL ----------

#         plan = create_plan(command)

#         print("\nExecution Plan:")

#         if isinstance(plan, dict):
#             print(plan)
#         else:
#             for step in plan:
#                 print(step)

#         speak("Executing")

#         # FIX-1
#         final_core.execute(plan)

#         speak("Done")

#         show_memory()


# if __name__ == "__main__":
#     start_fury()




from dotenv import load_dotenv
load_dotenv()

from execution.auto_loop import run_autonomous
from brain.context_memory import memory

from voice.speech_to_text import listen_once
from voice.text_to_speech import speak

from agents.register_agents import register_all_agents
from agents.jarvis_controller import jarvis
from core.final_core import final_core


voice_mode = False
jarvis_mode = False


# -------------------------
# MEMORY DISPLAY
# -------------------------

def show_memory():

    print("---- MEMORY ----")
    print("App:", memory.get_app())
    print("Window:", memory.get_window())
    print("Site:", memory.get_site())
    print("File:", memory.get_file())
    print("Action:", memory.get_action())
    print("----------------")


# -------------------------
# INPUT HANDLER
# -------------------------

def get_command():

    global voice_mode, jarvis_mode

    if jarvis_mode or voice_mode:
        text = listen_once()
        return text if text else ""

    return input(">>> ").strip()


# -------------------------
# MAIN LOOP
# -------------------------

def start_fury():

    global voice_mode, jarvis_mode

    print("=================================")
    print("🔥 FURY AI ASSISTANT STARTED")
    print("voice mode / jarvis mode / exit")
    print("=================================")

    register_all_agents()

    while True:

        command = get_command()

        if not command:
            continue

        cmd = command.lower().strip()

        # -------------------------
        # EXIT
        # -------------------------

        if cmd == "exit":
            speak("Shutting down")
            print("Shutting down Fury")
            break

        # -------------------------
        # MODES
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

        if cmd == "jarvis mode":

            jarvis_mode = True
            voice_mode = False
            speak("Jarvis mode activated")

            while jarvis_mode:

                text = listen_once()

                if not text:
                    continue

                if text.lower().strip() == "stop jarvis":
                    jarvis_mode = False
                    break

                jarvis.run_loop(text)

            continue

        # -------------------------
        # GOAL MODE
        # -------------------------

        if cmd.startswith("goal "):
            goal = command[5:].strip()
            speak("Goal mode")
            jarvis.run_loop(goal)
            continue

        # -------------------------
        # AUTO MODE
        # -------------------------

        if cmd.startswith("auto "):
            goal = command[5:].strip()
            speak("Autonomous mode")
            run_autonomous(goal)
            continue

        # =========================
        # MAIN PIPELINE
        # =========================

        print("\nSending to Agent System...")

        # context enrichment + execution happens inside final_core
        final_core.execute(command)

        show_memory()


# -------------------------
# ENTRY POINT
# -------------------------

if __name__ == "__main__":
    start_fury()