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


def show_memory():
    print("---- MEMORY ----")
    print("App:", memory.get_app())
    print("Window:", memory.get_window())
    print("Site:", memory.get_site())
    print("File:", memory.get_file())
    print("Action:", memory.get_action())
    print("----------------")


def get_command():
    global voice_mode, jarvis_mode
    if jarvis_mode or voice_mode:
        text = listen_once()
        return text if text else ""
    return input(">>> ").strip()


def start_fury():

    global voice_mode, jarvis_mode

    print("=================================")
    print("🔥 FURY AI ASSISTANT STARTED")
    print("Type 'fury help' for all commands")
    print("=================================")

    register_all_agents()

    while True:

        command = get_command()
        if not command:
            continue

        cmd = command.lower().strip()

        # EXIT
        if cmd == "exit":
            speak("Shutting down")
            print("Shutting down Fury")
            break

        # MODES
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

        # GOAL MODE
        if cmd.startswith("goal "):
            goal = command[5:].strip()
            speak("Goal mode")
            jarvis.run_loop(goal)
            continue

        # AUTO MODE
        if cmd.startswith("auto "):
            goal = command[5:].strip()
            speak("Autonomous mode")
            run_autonomous(goal)
            continue

        # -------------------------
        # STEP 131 — VISUAL MODE
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
        # STEP 132 — RESUME + HISTORY
        # -------------------------
        if cmd == "resume":
            from execution.visual_agent import resume_last_task
            from memory.task_memory import get_pending_task_summary
            summary = get_pending_task_summary()
            if summary:
                print(f"\nFury: Resuming — '{summary['goal']}'")
                print(f"      Completed {summary['steps_completed']} steps")
                print(f"      Saved at {summary['saved_at']}")
                resume_last_task()
            else:
                print("Fury: No interrupted task to resume.")
            continue

        if cmd in ("visual history", "fury visual history"):
            from memory.task_memory import print_history
            print_history()
            continue

        # -------------------------
        # STEP 133 — DECOMPOSE
        # -------------------------
        if cmd.startswith("decompose "):
            goal = command[10:].strip()
            from execution.goal_decomposer import decompose_goal, print_plan
            print(f"\n🧩 Decomposing: {goal}")
            plan = decompose_goal(goal)
            print_plan(plan)
            print("\nRun this plan? (yes/no)")
            answer = input(">>> ").strip().lower()
            if answer in ("yes", "y"):
                from execution.goal_decomposer import execute_plan
                execute_plan(plan)
            continue

        # -------------------------
        # STEP 134 — TAB INTELLIGENCE
        # -------------------------
        if cmd in ("tabs", "show tabs", "fury tabs"):
            from brain.tab_intelligence import print_open_tabs
            print_open_tabs()
            continue

        if cmd.startswith("switch to "):
            platform = cmd.replace("switch to ", "").strip()
            from brain.tab_intelligence import switch_to_tab
            switch_to_tab(platform)
            continue

        # -------------------------
        # STEP 135 — PERSONAL PROFILE
        # -------------------------
        if cmd in ("profile", "fury profile"):
            from brain.personal_profile import profile
            profile.show()
            continue

        if cmd == "fury profile reload":
            from brain.personal_profile import profile
            profile.reload()
            print("✅ Profile reloaded from profile.yaml")
            continue

        # -------------------------
        # STEP 136 — LEETCODE SOLVER
        # -------------------------
        if cmd.startswith("leetcode "):
            problem = command[9:].strip()
            from execution.visual_agent import run_visual_goal
            print(f"\n🧩 LeetCode: {problem}")
            result = run_visual_goal(f"solve leetcode problem {problem}")
            print(f"Outcome: {result['outcome']} in {result['steps']} steps")
            continue

        # -------------------------
        # STEP 137 — JOB APPLY
        # -------------------------
        if cmd.startswith("apply "):
            details = command[6:].strip()
            from execution.visual_agent import run_visual_goal
            from brain.personal_profile import profile
            ctx = profile.get_form_context()
            print(f"\n💼 Applying: {details}")
            result = run_visual_goal(f"apply to this job: {details}", context=ctx)
            print(f"Outcome: {result['outcome']} in {result['steps']} steps")
            continue

        # -------------------------
        # PERMISSIONS
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
voice mode / text mode        — input mode
jarvis mode                   — continuous voice loop
goal <task>                   — goal-based execution
auto <task>                   — autonomous mode

--- PHASE 10 — VISUAL AGENT ---
visual <goal>                 — visual agent (sees screen + acts)
resume                        — resume interrupted visual task
visual history                — show all visual tasks run
decompose <goal>              — break goal into steps then run

--- PLATFORM SHORTCUTS ---
leetcode <problem>            — solve a leetcode problem
apply <job details / url>     — apply to a job
switch to <platform>          — switch to open platform tab
tabs                          — show all open platform tabs

--- PROFILE ---
profile                       — show your personal profile
fury profile reload           — reload profile.yaml

--- PERMISSIONS ---
permissions                   — show all permissions
fury permission grant <cap>   — grant a capability
fury permission deny <cap>    — deny a capability
fury permission reset         — reset all permissions

--- DEBUG ---
fury stats                    — episode stats
fury patterns                 — pattern report
fury failures                 — commands needing fixes
fury knows <concept>          — knowledge graph lookup
fury help                     — show this help

--- VISUAL EXAMPLES ---
visual play lofi music on youtube
visual solve leetcode two sum
visual send whatsapp to John: hey
visual apply for react developer job on naukri
visual find full stack jobs on internshala
decompose apply to this job: <paste job url or description>
leetcode two sum
apply react developer naukri.com
=====================
""")
            continue

        # MAIN PIPELINE
        print("\nSending to Agent System...")
        final_core.execute(command)
        show_memory()


if __name__ == "__main__":
    start_fury()