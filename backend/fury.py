from execution.task_planner import create_plan
from execution.executor import execute_plan

from brain.context_memory import memory

# STEP 31 / 32
from voice.speech_to_text import listen_once
from voice.text_to_speech import speak


voice_mode = False


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

    global voice_mode

    if voice_mode:

        text = listen_once()

        if text:
            return text

        return ""

    else:

        return input(">>> ").strip()


# -----------------------------
# MAIN LOOP
# -----------------------------

def start_fury():

    global voice_mode

    print("=================================")
    print("🔥 FURY AI ASSISTANT STARTED")
    print("Type 'exit' to stop Fury")
    print("Type 'voice mode' to enable mic")
    print("=================================")

    while True:

        command = get_command()

        if not command:
            continue

        # -------------------------
        # EXIT
        # -------------------------

        if command.lower() == "exit":

            speak("Shutting down")

            print("Shutting down Fury...")

            break

        # -------------------------
        # VOICE MODE ON
        # -------------------------

        if command.lower() == "voice mode":

            voice_mode = True

            speak("Voice mode activated")

            print("Voice mode ON")

            continue

        # -------------------------
        # VOICE MODE OFF
        # -------------------------

        if command.lower() == "text mode":

            voice_mode = False

            speak("Text mode activated")

            print("Voice mode OFF")

            continue

        # -------------------------
        # CREATE PLAN
        # -------------------------

        plan = create_plan(command)

        print("\nExecution Plan:")

        if isinstance(plan, dict):
            print(plan)
        else:
            for step in plan:
                print(step)

        print()

        # -------------------------
        # EXECUTE
        # -------------------------

        speak("Executing")

        execute_plan(plan)

        speak("Done")

        # -------------------------
        # MEMORY
        # -------------------------

        show_memory()

        print()


# -----------------------------

if __name__ == "__main__":
    start_fury()