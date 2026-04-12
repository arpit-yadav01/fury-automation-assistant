
# from dotenv import load_dotenv
# load_dotenv()

# from execution.auto_loop import run_autonomous
# from brain.context_memory import memory

# from voice.speech_to_text import listen_once
# from voice.text_to_speech import speak

# from agents.register_agents import register_all_agents
# from agents.jarvis_controller import jarvis
# from core.final_core import final_core


# voice_mode = False
# jarvis_mode = False


# # -------------------------
# # MEMORY DISPLAY
# # -------------------------

# def show_memory():
#     print("---- MEMORY ----")
#     print("App:", memory.get_app())
#     print("Window:", memory.get_window())
#     print("Site:", memory.get_site())
#     print("File:", memory.get_file())
#     print("Action:", memory.get_action())
#     print("----------------")


# # -------------------------
# # INPUT HANDLER
# # -------------------------

# def get_command():
#     global voice_mode, jarvis_mode
#     if jarvis_mode or voice_mode:
#         text = listen_once()
#         return text if text else ""
#     return input(">>> ").strip()


# # -------------------------
# # MAIN LOOP
# # -------------------------

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

#         cmd = command.lower().strip()

#         # -------------------------
#         # EXIT
#         # -------------------------

#         if cmd == "exit":
#             speak("Shutting down")
#             print("Shutting down Fury")
#             break

#         # -------------------------
#         # MODES
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

#         if cmd == "jarvis mode":
#             jarvis_mode = True
#             voice_mode = False
#             speak("Jarvis mode activated")
#             while jarvis_mode:
#                 text = listen_once()
#                 if not text:
#                     continue
#                 if text.lower().strip() == "stop jarvis":
#                     jarvis_mode = False
#                     break
#                 jarvis.run_loop(text)
#             continue

#         # -------------------------
#         # GOAL MODE
#         # -------------------------

#         if cmd.startswith("goal "):
#             goal = command[5:].strip()
#             speak("Goal mode")
#             jarvis.run_loop(goal)
#             continue

#         # -------------------------
#         # AUTO MODE
#         # -------------------------

#         if cmd.startswith("auto "):
#             goal = command[5:].strip()
#             speak("Autonomous mode")
#             run_autonomous(goal)
#             continue

#         # -------------------------
#         # STEP 126 — PERMISSIONS
#         # -------------------------

#         if cmd in ("permissions", "show permissions"):
#             from core.permission_system import show_permissions
#             show_permissions()
#             continue

#         if cmd.startswith("fury permission grant "):
#             cap = cmd.replace("fury permission grant ", "").strip()
#             from core.permission_system import grant_permission
#             grant_permission(cap)
#             continue

#         if cmd.startswith("fury permission deny "):
#             cap = cmd.replace("fury permission deny ", "").strip()
#             from core.permission_system import deny_permission
#             deny_permission(cap)
#             continue

#         if cmd == "fury permission reset":
#             from core.permission_system import reset_permissions
#             reset_permissions()
#             continue

#         # -------------------------
#         # STATS / DEBUG
#         # -------------------------

#         if cmd == "fury stats":
#             final_core.show_stats()
#             continue

#         if cmd == "fury patterns":
#             final_core.show_patterns()
#             continue

#         if cmd == "fury failures":
#             final_core.show_failures()
#             continue

#         if cmd.startswith("fury knows "):
#             concept = cmd.replace("fury knows ", "").strip()
#             final_core.what_do_i_know(concept)
#             continue

#         if cmd == "fury help":
#             print("""
# === FURY COMMANDS ===
# exit                          — shutdown
# voice mode                    — switch to voice input
# text mode                     — switch to text input
# jarvis mode                   — continuous voice loop
# goal <task>                   — goal-based execution
# auto <task>                   — autonomous mode

# permissions                   — show all permissions
# fury permission grant <cap>   — grant a capability
# fury permission deny <cap>    — deny a capability
# fury permission reset          — reset all permissions

# fury stats                    — episode stats
# fury patterns                 — pattern report
# fury failures                 — commands that need fixing
# fury knows <concept>          — knowledge graph lookup
# fury help                     — show this help
# =====================
# """)
#             continue

#         # =========================
#         # MAIN PIPELINE
#         # =========================

#         print("\nSending to Agent System...")
#         final_core.execute(command)
#         show_memory()


# # -------------------------
# # ENTRY POINT
# # -------------------------

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

        # -------------------------
        # STEP 131 — VISUAL MODE
        # The real Phase 10 engine
        # Usage: visual <goal>
        # Examples:
        #   visual play lofi music on youtube
        #   visual solve leetcode problem 1
        #   visual send whatsapp message to john hello
        #   visual apply to this job on linkedin
        # -------------------------

        if cmd.startswith("visual "):
            goal = command[7:].strip()
            speak("Visual mode")
            print(f"\n🤖 Visual Agent — Goal: {goal}")
            from execution.visual_agent import run_visual_goal
            result = run_visual_goal(goal)
            print(f"Outcome: {result['outcome']} in {result['steps']} steps")
            continue

        # -------------------------
        # STEP 126 — PERMISSIONS
        # -------------------------

        if cmd in ("permissions", "show permissions"):
            from core.permission_system import show_permissions
            show_permissions()
            continue

        if cmd.startswith("fury permission grant "):
            cap = cmd.replace("fury permission grant ", "").strip()
            from core.permission_system import grant_permission
            grant_permission(cap)
            continue

        if cmd.startswith("fury permission deny "):
            cap = cmd.replace("fury permission deny ", "").strip()
            from core.permission_system import deny_permission
            deny_permission(cap)
            continue

        if cmd == "fury permission reset":
            from core.permission_system import reset_permissions
            reset_permissions()
            continue

        # -------------------------
        # STATS / DEBUG
        # -------------------------

        if cmd == "fury stats":
            final_core.show_stats()
            continue

        if cmd == "fury patterns":
            final_core.show_patterns()
            continue

        if cmd == "fury failures":
            final_core.show_failures()
            continue

        if cmd.startswith("fury knows "):
            concept = cmd.replace("fury knows ", "").strip()
            final_core.what_do_i_know(concept)
            continue

        if cmd == "fury help":
            print("""
=== FURY COMMANDS ===
exit                          — shutdown
voice mode                    — switch to voice input
text mode                     — switch to text input
jarvis mode                   — continuous voice loop
goal <task>                   — goal-based execution
auto <task>                   — autonomous mode
visual <goal>                 — visual agent (Phase 10)

permissions                   — show all permissions
fury permission grant <cap>   — grant a capability
fury permission deny <cap>    — deny a capability
fury permission reset         — reset all permissions

fury stats                    — episode stats
fury patterns                 — pattern report
fury failures                 — commands that need fixing
fury knows <concept>          — knowledge graph lookup
fury help                     — show this help

--- VISUAL MODE EXAMPLES ---
visual play lofi music on youtube
visual solve leetcode problem two sum
visual send whatsapp message to John: hey
visual find movie inception on any site
visual apply to software engineer job on linkedin
=====================
""")
            continue

        # =========================
        # MAIN PIPELINE
        # =========================

        print("\nSending to Agent System...")
        final_core.execute(command)
        show_memory()


# -------------------------
# ENTRY POINT
# -------------------------

if __name__ == "__main__":
    start_fury()