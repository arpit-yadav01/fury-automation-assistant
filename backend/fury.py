
# # from dotenv import load_dotenv
# # load_dotenv()

# # from execution.auto_loop import run_autonomous
# # from brain.context_memory import memory

# # from voice.speech_to_text import listen_once
# # from voice.text_to_speech import speak

# # from agents.register_agents import register_all_agents
# # from agents.jarvis_controller import jarvis
# # from core.final_core import final_core


# # voice_mode = False
# # jarvis_mode = False


# # # -------------------------
# # # MEMORY DISPLAY
# # # -------------------------

# # def show_memory():
# #     print("---- MEMORY ----")
# #     print("App:", memory.get_app())
# #     print("Window:", memory.get_window())
# #     print("Site:", memory.get_site())
# #     print("File:", memory.get_file())
# #     print("Action:", memory.get_action())
# #     print("----------------")


# # # -------------------------
# # # INPUT HANDLER
# # # -------------------------

# # def get_command():
# #     global voice_mode, jarvis_mode
# #     if jarvis_mode or voice_mode:
# #         text = listen_once()
# #         return text if text else ""
# #     return input(">>> ").strip()


# # # -------------------------
# # # MAIN LOOP
# # # -------------------------

# # def start_fury():

# #     global voice_mode, jarvis_mode

# #     print("=================================")
# #     print("🔥 FURY AI ASSISTANT STARTED")
# #     print("voice mode / jarvis mode / exit")
# #     print("=================================")

# #     register_all_agents()

# #     while True:

# #         command = get_command()

# #         if not command:
# #             continue

# #         cmd = command.lower().strip()

# #         # -------------------------
# #         # EXIT
# #         # -------------------------

# #         if cmd == "exit":
# #             speak("Shutting down")
# #             print("Shutting down Fury")
# #             break

# #         # -------------------------
# #         # MODES
# #         # -------------------------

# #         if cmd == "voice mode":
# #             voice_mode = True
# #             jarvis_mode = False
# #             speak("Voice mode activated")
# #             continue

# #         if cmd == "text mode":
# #             voice_mode = False
# #             jarvis_mode = False
# #             speak("Text mode")
# #             continue

# #         if cmd == "jarvis mode":
# #             jarvis_mode = True
# #             voice_mode = False
# #             speak("Jarvis mode activated")
# #             while jarvis_mode:
# #                 text = listen_once()
# #                 if not text:
# #                     continue
# #                 if text.lower().strip() == "stop jarvis":
# #                     jarvis_mode = False
# #                     break
# #                 jarvis.run_loop(text)
# #             continue

# #         # -------------------------
# #         # GOAL MODE
# #         # -------------------------

# #         if cmd.startswith("goal "):
# #             goal = command[5:].strip()
# #             speak("Goal mode")
# #             jarvis.run_loop(goal)
# #             continue

# #         # -------------------------
# #         # AUTO MODE
# #         # -------------------------

# #         if cmd.startswith("auto "):
# #             goal = command[5:].strip()
# #             speak("Autonomous mode")
# #             run_autonomous(goal)
# #             continue

# #         # -------------------------
# #         # STEP 126 — PERMISSIONS
# #         # -------------------------

# #         if cmd in ("permissions", "show permissions"):
# #             from core.permission_system import show_permissions
# #             show_permissions()
# #             continue

# #         if cmd.startswith("fury permission grant "):
# #             cap = cmd.replace("fury permission grant ", "").strip()
# #             from core.permission_system import grant_permission
# #             grant_permission(cap)
# #             continue

# #         if cmd.startswith("fury permission deny "):
# #             cap = cmd.replace("fury permission deny ", "").strip()
# #             from core.permission_system import deny_permission
# #             deny_permission(cap)
# #             continue

# #         if cmd == "fury permission reset":
# #             from core.permission_system import reset_permissions
# #             reset_permissions()
# #             continue

# #         # -------------------------
# #         # STATS / DEBUG
# #         # -------------------------

# #         if cmd == "fury stats":
# #             final_core.show_stats()
# #             continue

# #         if cmd == "fury patterns":
# #             final_core.show_patterns()
# #             continue

# #         if cmd == "fury failures":
# #             final_core.show_failures()
# #             continue

# #         if cmd.startswith("fury knows "):
# #             concept = cmd.replace("fury knows ", "").strip()
# #             final_core.what_do_i_know(concept)
# #             continue

# #         if cmd == "fury help":
# #             print("""
# # === FURY COMMANDS ===
# # exit                          — shutdown
# # voice mode                    — switch to voice input
# # text mode                     — switch to text input
# # jarvis mode                   — continuous voice loop
# # goal <task>                   — goal-based execution
# # auto <task>                   — autonomous mode

# # permissions                   — show all permissions
# # fury permission grant <cap>   — grant a capability
# # fury permission deny <cap>    — deny a capability
# # fury permission reset          — reset all permissions

# # fury stats                    — episode stats
# # fury patterns                 — pattern report
# # fury failures                 — commands that need fixing
# # fury knows <concept>          — knowledge graph lookup
# # fury help                     — show this help
# # =====================
# # """)
# #             continue

# #         # =========================
# #         # MAIN PIPELINE
# #         # =========================

# #         print("\nSending to Agent System...")
# #         final_core.execute(command)
# #         show_memory()


# # # -------------------------
# # # ENTRY POINT
# # # -------------------------

# # if __name__ == "__main__":
# #     start_fury()




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
#     if jarvis_mode or voice_mode:
#         text = listen_once()
#         return text if text else ""
#     return input(">>> ").strip()


# def start_fury():

#     global voice_mode, jarvis_mode

#     print("=================================")
#     print("🔥 FURY AI ASSISTANT STARTED")
#     print("Type 'fury help' for all commands")
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

#         if cmd.startswith("goal "):
#             goal = command[5:].strip()
#             speak("Goal mode")
#             jarvis.run_loop(goal)
#             continue

#         if cmd.startswith("auto "):
#             goal = command[5:].strip()
#             speak("Autonomous mode")
#             run_autonomous(goal)
#             continue

#         # -------------------------
#         # STEP 131 — VISUAL MODE
#         # -------------------------
#         if cmd.startswith("visual "):
#             goal = command[7:].strip()
#             speak("Visual mode")
#             print(f"\n🤖 Visual Agent — Goal: {goal}")
#             from execution.visual_agent import run_visual_goal
#             result = run_visual_goal(goal)
#             print(f"Outcome: {result['outcome']} in {result['steps']} steps")
#             continue

#         # -------------------------
#         # STEP 132 — RESUME + HISTORY
#         # -------------------------
#         if cmd == "resume":
#             from execution.visual_agent import resume_last_task
#             from memory.task_memory import get_pending_task_summary
#             summary = get_pending_task_summary()
#             if summary:
#                 print(f"\nFury: Resuming — '{summary['goal']}'")
#                 print(f"      Completed {summary['steps_completed']} steps")
#                 print(f"      Saved at {summary['saved_at']}")
#                 resume_last_task()
#             else:
#                 print("Fury: No interrupted task to resume.")
#             continue

#         if cmd in ("visual history", "fury visual history"):
#             from memory.task_memory import print_history
#             print_history()
#             continue

#         # -------------------------
#         # STEP 133 — DECOMPOSE
#         # -------------------------
#         if cmd.startswith("decompose "):
#             goal = command[10:].strip()
#             from execution.goal_decomposer import decompose_goal, print_plan
#             print(f"\n🧩 Decomposing: {goal}")
#             plan = decompose_goal(goal)
#             print_plan(plan)
#             print("\nRun this plan? (yes/no)")
#             answer = input(">>> ").strip().lower()
#             if answer in ("yes", "y"):
#                 from execution.goal_decomposer import execute_plan
#                 execute_plan(plan)
#             continue

#         # -------------------------
#         # STEP 134 — TAB INTELLIGENCE
#         # -------------------------
#         if cmd in ("tabs", "show tabs", "fury tabs"):
#             from brain.tab_intelligence import print_open_tabs
#             print_open_tabs()
#             continue

#         if cmd.startswith("switch to "):
#             platform = cmd.replace("switch to ", "").strip()
#             from brain.tab_intelligence import switch_to_tab
#             switch_to_tab(platform)
#             continue

#         # -------------------------
#         # STEP 135 — PERSONAL PROFILE
#         # -------------------------
#         if cmd in ("profile", "fury profile"):
#             from brain.personal_profile import profile
#             profile.show()
#             continue

#         if cmd == "fury profile reload":
#             from brain.personal_profile import profile
#             profile.reload()
#             print("✅ Profile reloaded from profile.yaml")
#             continue

#         # -------------------------
#         # STEP 136 — LEETCODE SOLVER
#         # -------------------------
#         if cmd.startswith("leetcode "):
#             problem = command[9:].strip()
#             from execution.visual_agent import run_visual_goal
#             print(f"\n🧩 LeetCode: {problem}")
#             result = run_visual_goal(f"solve leetcode problem {problem}")
#             print(f"Outcome: {result['outcome']} in {result['steps']} steps")
#             continue

#         # -------------------------
#         # STEP 137 — JOB APPLY
#         # -------------------------
#         if cmd.startswith("apply "):
#             details = command[6:].strip()
#             from execution.visual_agent import run_visual_goal
#             from brain.personal_profile import profile
#             ctx = profile.get_form_context()
#             print(f"\n💼 Applying: {details}")
#             result = run_visual_goal(f"apply to this job: {details}", context=ctx)
#             print(f"Outcome: {result['outcome']} in {result['steps']} steps")
#             continue

#         # -------------------------
#         # STEP 138 — GMAIL AGENT
#         # -------------------------
#         if cmd in ("check email", "read email", "gmail"):
#             from agents.platforms.gmail_agent import gmail
#             gmail.read_emails()
#             continue

#         if cmd == "check unread":
#             from agents.platforms.gmail_agent import gmail
#             gmail.check_unread()
#             continue

#         if cmd.startswith("send email to "):
#             # format: send email to friend@gmail.com subject: Hello body: How are you?
#             rest = command[14:].strip()
#             parts = rest.split(" subject: ")
#             to = parts[0].strip()
#             if len(parts) > 1:
#                 body_parts = parts[1].split(" body: ")
#                 subject = body_parts[0].strip()
#                 body    = body_parts[1].strip() if len(body_parts) > 1 else ""
#             else:
#                 subject = "Message from Fury"
#                 body    = rest
#             from agents.platforms.gmail_agent import gmail
#             gmail.send(to, subject, body)
#             continue

#         if cmd.startswith("reply to "):
#             # format: reply to John Thanks for reaching out
#             rest   = command[9:].strip()
#             parts  = rest.split(" ", 1)
#             sender = parts[0].strip()
#             reply  = parts[1].strip() if len(parts) > 1 else ""
#             from agents.platforms.gmail_agent import gmail
#             gmail.reply_to_email(sender, reply)
#             continue

#         if cmd.startswith("compose email "):
#             # format: compose email to friend@gmail.com about follow up on my interview
#             rest   = command[14:].strip()
#             parts  = rest.split(" about ")
#             to     = parts[0].replace("to ", "").strip()
#             instr  = parts[1].strip() if len(parts) > 1 else rest
#             from agents.platforms.gmail_agent import gmail
#             gmail.compose_with_ai(to, "Message from Arpit", instr)
#             continue

#         # -------------------------
#         # STEP 139 — WHATSAPP AGENT
#         # -------------------------
#         if cmd.startswith("whatsapp ") or cmd.startswith("send whatsapp "):
#             # format: whatsapp John hey how are you
#             # format: send whatsapp to John: hey how are you
#             rest = command.replace("send whatsapp to ", "").replace("whatsapp ", "").strip()
#             if ":" in rest:
#                 parts   = rest.split(":", 1)
#                 contact = parts[0].strip()
#                 message = parts[1].strip()
#             else:
#                 parts   = rest.split(" ", 1)
#                 contact = parts[0].strip()
#                 message = parts[1].strip() if len(parts) > 1 else ""
#             from agents.platforms.whatsapp_agent import whatsapp
#             whatsapp.send(contact, message)
#             continue

#         if cmd.startswith("read whatsapp "):
#             contact = command[14:].strip()
#             from agents.platforms.whatsapp_agent import whatsapp
#             whatsapp.read(contact)
#             continue

#         if cmd.startswith("reply whatsapp "):
#             rest    = command[15:].strip()
#             parts   = rest.split(" ", 1)
#             contact = parts[0].strip()
#             reply   = parts[1].strip() if len(parts) > 1 else ""
#             from agents.platforms.whatsapp_agent import whatsapp
#             whatsapp.reply_last(contact, reply)
#             continue

#         if cmd in ("whatsapp unread", "check whatsapp"):
#             from agents.platforms.whatsapp_agent import whatsapp
#             whatsapp.check_unread()
#             continue

#         # -------------------------
#         # STEP 140 — TELEGRAM AGENT
#         # -------------------------
#         if cmd.startswith("telegram ") or cmd.startswith("send telegram "):
#             # format: telegram John hey how are you
#             # format: send telegram to John: message
#             rest = command.replace("send telegram to ", "").replace("telegram ", "").strip()
#             if ":" in rest:
#                 parts   = rest.split(":", 1)
#                 contact = parts[0].strip()
#                 message = parts[1].strip()
#             else:
#                 parts   = rest.split(" ", 1)
#                 contact = parts[0].strip()
#                 message = parts[1].strip() if len(parts) > 1 else ""
#             from agents.platforms.telegram_agent import telegram
#             telegram.send(contact, message)
#             continue

#         if cmd.startswith("read telegram "):
#             contact = command[14:].strip()
#             from agents.platforms.telegram_agent import telegram
#             telegram.read(contact)
#             continue

#         if cmd.startswith("reply telegram "):
#             rest    = command[15:].strip()
#             parts   = rest.split(" ", 1)
#             contact = parts[0].strip()
#             reply   = parts[1].strip() if len(parts) > 1 else ""
#             from agents.platforms.telegram_agent import telegram
#             telegram.reply_last(contact, reply)
#             continue

#         if cmd in ("telegram unread", "check telegram"):
#             from agents.platforms.telegram_agent import telegram
#             telegram.check_unread()
#             continue

#         # -------------------------
#         # PERMISSIONS
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
# voice mode / text mode        — input mode
# jarvis mode                   — continuous voice loop
# goal <task>                   — goal-based execution
# auto <task>                   — autonomous mode

# --- PHASE 10 — VISUAL AGENT ---
# visual <goal>                 — visual agent (sees screen + acts)
# resume                        — resume interrupted visual task
# visual history                — show all visual tasks run
# decompose <goal>              — break goal into steps then run

# --- PLATFORM SHORTCUTS ---
# leetcode <problem>            — solve a leetcode problem
# apply <job details / url>     — apply to a job on any platform
# switch to <platform>          — switch to open platform tab
# tabs                          — show all open platform tabs

# --- GMAIL (Step 138) ---
# check email                   — read and summarize inbox
# check unread                  — quick unread count
# send email to <email> subject: <s> body: <b>
# reply to <name> <message>
# compose email to <email> about <what to say>

# --- WHATSAPP (Step 139) ---
# whatsapp <contact> <message>
# read whatsapp <contact>
# reply whatsapp <contact> <message>
# check whatsapp                — show unread chats

# --- TELEGRAM (Step 140) ---
# telegram <contact> <message>
# read telegram <contact>
# reply telegram <contact> <message>
# check telegram                — show unread chats

# --- PROFILE ---
# profile                       — show your personal profile
# fury profile reload           — reload profile.yaml

# --- PERMISSIONS ---
# permissions                   — show all permissions
# fury permission grant <cap>   — grant a capability
# fury permission deny <cap>    — deny a capability
# fury permission reset         — reset all permissions

# --- DEBUG ---
# fury stats                    — episode stats
# fury patterns                 — pattern report
# fury failures                 — commands needing fixes
# fury knows <concept>          — knowledge graph lookup
# fury help                     — show this help

# --- EXAMPLES ---
# visual play lofi music on youtube
# visual solve leetcode two sum
# leetcode two sum
# apply react developer naukri.com
# check email
# send email to hr@company.com subject: Job Application body: I am applying for the React Developer role
# whatsapp John hey are you free tonight?
# telegram DevGroup daily update ready
# =====================
# """)
#             continue

#         # -------------------------
#         # MAIN PIPELINE
#         # -------------------------
#         print("\nSending to Agent System...")
#         final_core.execute(command)
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

        while command.startswith(">"):
            command = command.lstrip("> ").strip()
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
            voice_mode = True; jarvis_mode = False
            speak("Voice mode activated")
            continue

        if cmd == "text mode":
            voice_mode = False; jarvis_mode = False
            speak("Text mode")
            continue

        if cmd == "jarvis mode":
            jarvis_mode = True; voice_mode = False
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

        if cmd.startswith("goal "):
            jarvis.run_loop(command[5:].strip())
            continue

        if cmd.startswith("auto "):
            run_autonomous(command[5:].strip())
            continue

        # ─────────────────────────────
        # STEP 131 — VISUAL MODE
        # ─────────────────────────────
        if cmd.startswith("visual "):
            from execution.visual_agent import run_visual_goal
            result = run_visual_goal(command[7:].strip())
            print(f"Outcome: {result['outcome']} in {result['steps']} steps")
            continue

        # ─────────────────────────────
        # STEP 132 — RESUME + HISTORY
        # ─────────────────────────────
        if cmd == "resume":
            from execution.visual_agent import resume_last_task
            from memory.task_memory import get_pending_task_summary
            summary = get_pending_task_summary()
            if summary:
                print(f"Resuming: '{summary['goal']}'")
                resume_last_task()
            else:
                print("No interrupted task.")
            continue

        if cmd in ("visual history", "fury visual history"):
            from memory.task_memory import print_history
            print_history()
            continue

        # ─────────────────────────────
        # STEP 133 — DECOMPOSE
        # ─────────────────────────────
        if cmd.startswith("decompose "):
            from execution.goal_decomposer import decompose_goal, print_plan
            plan = decompose_goal(command[10:].strip())
            print_plan(plan)
            print("Run this plan? (yes/no)")
            if input(">>> ").strip().lower() in ("yes", "y"):
                from execution.goal_decomposer import execute_plan
                execute_plan(plan)
            continue

        # ─────────────────────────────
        # STEP 134 — TABS
        # ─────────────────────────────
        if cmd in ("tabs", "show tabs", "fury tabs"):
            from brain.tab_intelligence import print_open_tabs
            print_open_tabs()
            continue

        if cmd.startswith("switch to "):
            from brain.tab_intelligence import switch_to_tab
            switch_to_tab(cmd.replace("switch to ", "").strip())
            continue

        # ─────────────────────────────
        # STEP 135 — PROFILE
        # ─────────────────────────────
        if cmd in ("profile", "fury profile"):
            from brain.personal_profile import profile
            profile.show()
            continue

        if cmd == "fury profile reload":
            from brain.personal_profile import profile
            profile.reload()
            print("✅ Profile reloaded")
            continue

        # ─────────────────────────────
        # STEP 136 + 143 — LEETCODE
        # leetcode <problem>        → open only
        # leetcode solve <problem>  → open + generate + type + run
        # leetcode submit <problem> → open + generate + type + run + submit
        # ─────────────────────────────
        if cmd.startswith("leetcode "):
            problem = command[9:].strip()
            slug    = problem.lower().replace(" ", "-")

            if cmd.startswith("leetcode solve "):
                problem = command[15:].strip()
                from platforms.leetcode_solver import solve_leetcode
                print(f"\n🧩 Solving: {problem}")
                result = solve_leetcode(problem, auto_submit=False)
                print(f"Outcome: {result['outcome']}")

            elif cmd.startswith("leetcode submit "):
                problem = command[16:].strip()
                from platforms.leetcode_solver import solve_leetcode
                print(f"\n🧩 Solving + submitting: {problem}")
                result = solve_leetcode(problem, auto_submit=True)
                print(f"Outcome: {result['outcome']}")

            else:
                url = f"https://leetcode.com/problems/{slug}/"
                from execution.visual_agent import run_visual_goal
                print(f"\n🧩 LeetCode: {problem} → {url}")
                result = run_visual_goal(
                    f"open leetcode problem {problem}",
                    context={"platform": "leetcode", "slug": slug, "url": url}
                )
                print(f"Outcome: {result['outcome']} in {result['steps']} steps")
            continue

        # ─────────────────────────────
        # STEP 137 — JOB SEARCH (safe)
        # ─────────────────────────────
        if cmd.startswith("search jobs "):
            rest  = command[12:].strip()
            known = ["naukri","indeed","internshala","linkedin",
                     "monster","unstop","wellfound"]
            parts = rest.rsplit(" ", 1)
            if len(parts) == 2 and parts[1].lower() in known:
                query, platform = parts[0].strip(), parts[1].lower()
            else:
                query, platform = rest, "naukri"
            from platforms.job_search_agent import search_jobs
            search_jobs(query, platform)
            continue

        if cmd.startswith("read job "):
            from platforms.job_search_agent import read_job_details
            read_job_details(command[9:].strip())
            continue

        # ─────────────────────────────
        # STEP 141 — JOB DESC PARSER
        # Paste any job description → cover letter + email
        # ─────────────────────────────
        if len(command) > 200 and any(kw in cmd for kw in [
            "experience", "required", "skills", "developer", "engineer",
            "responsibilities", "qualification", "salary", "apply",
            "role", "position", "hiring", "vacancy"
        ]):
            from platforms.job_desc_parser import parse_and_generate
            print("\n📋 Job description detected — generating cover letter + email...")
            parse_and_generate(command)
            continue

        if cmd.startswith("parse job "):
            from platforms.job_desc_parser import parse_and_generate
            parse_and_generate(command[10:].strip())
            continue

        if cmd.startswith("cover letter for "):
            rest    = command[17:].strip()
            parts   = rest.split(" at ", 1)
            role    = parts[0].strip()
            company = parts[1].strip() if len(parts) > 1 else "the company"
            from platforms.job_desc_parser import (
                generate_cover_letter, generate_email, _print_results
            )
            details = {"role": role, "company": company, "skills": [], "raw": ""}
            _print_results(details, generate_cover_letter(details), generate_email(details))
            continue

        if cmd.startswith("write cover letter "):
            rest    = command[19:].strip().split(" ", 1)
            role    = rest[0]
            company = rest[1] if len(rest) > 1 else "the company"
            from platforms.job_search_agent import generate_cover_letter
            generate_cover_letter(role, company)
            continue

        if cmd.startswith("draft email "):
            rest    = command[12:].strip().split(" ", 2)
            to      = rest[0] if rest else ""
            role    = rest[1] if len(rest) > 1 else "Developer"
            company = rest[2] if len(rest) > 2 else "the company"
            from platforms.job_search_agent import draft_email
            draft_email(to, role, company)
            continue

        # ─────────────────────────────
        # STEP 142 — CODE ASSISTANT
        # ─────────────────────────────
        if cmd.startswith("explain ") and any(
            cmd.endswith(e) for e in [".py",".js",".jsx",".ts",".tsx",".yaml",".json"]
        ):
            from developer.code_assistant import explain_file
            explain_file(command[8:].strip())
            continue

        if cmd.startswith("fix bug in ") or cmd.startswith("fix error in "):
            fp = cmd.replace("fix bug in ","").replace("fix error in ","").strip()
            from developer.code_assistant import fix_bug
            fix_bug(fp)
            continue

        if cmd.startswith("review ") and "." in cmd:
            from developer.code_assistant import review_code
            review_code(command[7:].strip())
            continue

        if cmd in ("list files",) or cmd.startswith("list files in "):
            from developer.code_assistant import handle_code_command
            handle_code_command(command)
            continue

        if cmd.startswith("code "):
            from developer.code_assistant import handle_code_command
            handle_code_command(command[5:].strip())
            continue

        # ─────────────────────────────
        # GMAIL
        # ─────────────────────────────
        if cmd in ("check email", "read email", "gmail"):
            from execution.visual_agent import run_visual_goal
            run_visual_goal("open gmail inbox", context={"platform": "gmail"})
            continue

        if cmd.startswith("compose email "):
            rest  = command[14:].strip().split(" about ")
            to    = rest[0].replace("to ", "").strip()
            instr = rest[1].strip() if len(rest) > 1 else command[14:]
            from platforms.gmail_agent import gmail
            gmail.compose_with_ai(to, "Message from Arpit", instr)
            continue

        # ─────────────────────────────
        # WHATSAPP
        # ─────────────────────────────
        if cmd.startswith("whatsapp ") or cmd.startswith("send whatsapp "):
            rest = command.replace("send whatsapp to ","").replace("whatsapp ","").strip()
            if ":" in rest:
                contact, message = rest.split(":", 1)
            else:
                parts = rest.split(" ", 1)
                contact = parts[0]
                message = parts[1] if len(parts) > 1 else ""
            from execution.visual_agent import run_visual_goal
            run_visual_goal(
                f"send whatsapp message to {contact.strip()}: {message.strip()}",
                context={"platform": "whatsapp", "contact": contact.strip()}
            )
            continue

        if cmd.startswith("read whatsapp "):
            from execution.visual_agent import run_visual_goal
            run_visual_goal(
                f"read whatsapp messages from {command[14:].strip()}",
                context={"platform": "whatsapp"}
            )
            continue

        if cmd in ("check whatsapp", "whatsapp unread"):
            from execution.visual_agent import run_visual_goal
            run_visual_goal("check whatsapp unread messages",
                            context={"platform": "whatsapp"})
            continue

        # ─────────────────────────────
        # TELEGRAM
        # ─────────────────────────────
        if cmd.startswith("telegram ") or cmd.startswith("send telegram "):
            rest = command.replace("send telegram to ","").replace("telegram ","").strip()
            if ":" in rest:
                contact, message = rest.split(":", 1)
            else:
                parts = rest.split(" ", 1)
                contact = parts[0]
                message = parts[1] if len(parts) > 1 else ""
            from execution.visual_agent import run_visual_goal
            run_visual_goal(
                f"send telegram to {contact.strip()}: {message.strip()}",
                context={"platform": "telegram", "contact": contact.strip()}
            )
            continue

        if cmd in ("check telegram", "telegram unread"):
            from execution.visual_agent import run_visual_goal
            run_visual_goal("check telegram unread",
                            context={"platform": "telegram"})
            continue

        # ─────────────────────────────
        # PERMISSIONS
        # ─────────────────────────────
        if cmd in ("permissions", "show permissions"):
            from core.permission_system import show_permissions
            show_permissions()
            continue

        if cmd.startswith("fury permission grant "):
            from core.permission_system import grant_permission
            grant_permission(cmd.replace("fury permission grant ","").strip())
            continue

        if cmd.startswith("fury permission deny "):
            from core.permission_system import deny_permission
            deny_permission(cmd.replace("fury permission deny ","").strip())
            continue

        if cmd == "fury permission reset":
            from core.permission_system import reset_permissions
            reset_permissions()
            continue

        # ─────────────────────────────
        # DEBUG
        # ─────────────────────────────
        if cmd == "fury stats":
            final_core.show_stats(); continue
        if cmd == "fury patterns":
            final_core.show_patterns(); continue
        if cmd == "fury failures":
            final_core.show_failures(); continue
        if cmd.startswith("fury knows "):
            final_core.what_do_i_know(cmd.replace("fury knows ","").strip())
            continue

        if cmd == "fury help":
            print("""
=== FURY COMMANDS ===
exit / voice mode / text mode / jarvis mode

--- VISUAL AGENT ---
visual <goal>               e.g. visual play lofi on youtube
resume / visual history
decompose <goal>

--- LEETCODE (Step 136 + 143) ---
leetcode <problem>          open only  e.g. leetcode two sum
leetcode solve <problem>    open + generate solution + run
leetcode submit <problem>   open + generate + run + submit

--- JOB TOOLS (safe — read only) ---
search jobs <role> <platform>
cover letter for <role> at <company>
write cover letter <role> <company>
draft email <email> <role> <company>
[paste any job description]     ← auto-detected

--- CODE ASSISTANT (Step 142) ---
explain <file.py>
fix bug in <file.py>
review <file.py>
list files
code <anything about your code>

--- MESSAGING ---
whatsapp <contact> <message>
check whatsapp
telegram <contact> <message>
check telegram
check email

--- PROFILE & TABS ---
profile / fury profile reload
tabs / switch to <platform>

--- PERMISSIONS ---
permissions
fury permission grant/deny <cap>

--- DEBUG ---
fury stats / fury patterns / fury failures
fury help
=====================
""")
            continue

        # MAIN PIPELINE
        print("\nSending to Agent System...")
        final_core.execute(command)
        show_memory()


if __name__ == "__main__":
    start_fury()