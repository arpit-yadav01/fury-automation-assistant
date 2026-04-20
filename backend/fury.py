
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

        if cmd == "exit":
            speak("Shutting down")
            print("Shutting down Fury")
            break

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

        # -------------------------
        # VISUAL MODE
        # -------------------------
        if cmd.startswith("visual "):
            goal = command[7:].strip()
            print(f"\n🤖 Visual Agent — Goal: {goal}")
            from execution.visual_agent import run_visual_goal
            result = run_visual_goal(goal)
            print(f"Outcome: {result['outcome']} in {result['steps']} steps")
            continue

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

        if cmd.startswith("decompose "):
            goal = command[10:].strip()
            from execution.goal_decomposer import decompose_goal, print_plan
            plan = decompose_goal(goal)
            print_plan(plan)
            print("Run this plan? (yes/no)")
            if input(">>> ").strip().lower() in ("yes", "y"):
                from execution.goal_decomposer import execute_plan
                execute_plan(plan)
            continue

        # -------------------------
        # TABS
        # -------------------------
        if cmd in ("tabs", "show tabs", "fury tabs"):
            from brain.tab_intelligence import print_open_tabs
            print_open_tabs()
            continue

        if cmd.startswith("switch to "):
            from brain.tab_intelligence import switch_to_tab
            switch_to_tab(cmd.replace("switch to ", "").strip())
            continue

        # -------------------------
        # PROFILE
        # -------------------------
        if cmd in ("profile", "fury profile"):
            from brain.personal_profile import profile
            profile.show()
            continue

        if cmd == "fury profile reload":
            from brain.personal_profile import profile
            profile.reload()
            print("✅ Profile reloaded")
            continue

        # -------------------------
        # LEETCODE
        # -------------------------
        if cmd.startswith("leetcode "):
            problem = command[9:].strip()
            slug = problem.lower().strip().replace(" ", "-")
            url  = f"https://leetcode.com/problems/{slug}/"
            from execution.visual_agent import run_visual_goal
            print(f"\n🧩 LeetCode: {problem} → {url}")
            result = run_visual_goal(
                f"open leetcode problem {problem}",
                context={"platform": "leetcode", "slug": slug, "url": url}
            )
            print(f"Outcome: {result['outcome']} in {result['steps']} steps")
            continue

        # -------------------------
        # JOB SEARCH — safe, read only
        # -------------------------
        if cmd.startswith("search jobs "):
            # format: search jobs react developer naukri
            rest  = command[12:].strip()
            parts = rest.rsplit(" ", 1)
            known = ["naukri","indeed","internshala","linkedin",
                     "monster","unstop","wellfound"]
            if len(parts) == 2 and parts[1].lower() in known:
                query    = parts[0].strip()
                platform = parts[1].lower()
            else:
                query    = rest
                platform = "naukri"
            from platforms.job_search_agent import search_jobs
            search_jobs(query, platform)
            continue

        if cmd.startswith("read job "):
            url = command[9:].strip()
            from platforms.job_search_agent import read_job_details
            read_job_details(url)
            continue

        if cmd.startswith("write cover letter "):
            # format: write cover letter React Developer TechCorp
            rest  = command[19:].strip()
            parts = rest.split(" ", 2)
            role    = parts[0] if len(parts) > 0 else "Developer"
            company = parts[1] if len(parts) > 1 else "the company"
            from platforms.job_search_agent import generate_cover_letter
            generate_cover_letter(role, company)
            continue

        if cmd.startswith("draft email "):
            # format: draft email hr@company.com React Developer TechCorp
            rest  = command[12:].strip()
            parts = rest.split(" ", 2)
            to      = parts[0] if len(parts) > 0 else ""
            role    = parts[1] if len(parts) > 1 else "Developer"
            company = parts[2] if len(parts) > 2 else "the company"
            from platforms.job_search_agent import draft_email
            draft_email(to, role, company)
            continue

        # -------------------------
        # GMAIL — read + draft only
        # -------------------------
        if cmd in ("check email", "read email", "gmail"):
            from execution.visual_agent import run_visual_goal
            run_visual_goal("open gmail and show inbox",
                            context={"platform": "gmail"})
            continue

        if cmd.startswith("compose email "):
            # generates draft — you send manually
            rest  = command[14:].strip()
            parts = rest.split(" about ")
            to    = parts[0].replace("to ", "").strip()
            instr = parts[1].strip() if len(parts) > 1 else rest
            from platforms.gmail_agent import gmail
            gmail.compose_with_ai(to, "Message from Arpit", instr)
            continue

        # -------------------------
        # WHATSAPP
        # -------------------------
        if cmd.startswith("whatsapp ") or cmd.startswith("send whatsapp "):
            rest = command.replace("send whatsapp to ", "").replace("whatsapp ", "").strip()
            if ":" in rest:
                contact, message = rest.split(":", 1)
            else:
                parts = rest.split(" ", 1)
                contact = parts[0]
                message = parts[1] if len(parts) > 1 else ""
            contact = contact.strip()
            message = message.strip()
            from execution.visual_agent import run_visual_goal
            print(f"\n💬 WhatsApp → {contact}: {message}")
            run_visual_goal(
                f"send whatsapp message to {contact}: {message}",
                context={"platform": "whatsapp", "contact": contact}
            )
            continue

        if cmd.startswith("read whatsapp "):
            contact = command[14:].strip()
            from execution.visual_agent import run_visual_goal
            run_visual_goal(
                f"read whatsapp messages from {contact}",
                context={"platform": "whatsapp", "contact": contact}
            )
            continue

        if cmd in ("check whatsapp", "whatsapp unread"):
            from execution.visual_agent import run_visual_goal
            run_visual_goal("check whatsapp unread messages",
                            context={"platform": "whatsapp"})
            continue

        # -------------------------
        # TELEGRAM
        # -------------------------
        if cmd.startswith("telegram ") or cmd.startswith("send telegram "):
            rest = command.replace("send telegram to ", "").replace("telegram ", "").strip()
            if ":" in rest:
                contact, message = rest.split(":", 1)
            else:
                parts = rest.split(" ", 1)
                contact = parts[0]
                message = parts[1] if len(parts) > 1 else ""
            from execution.visual_agent import run_visual_goal
            run_visual_goal(
                f"send telegram message to {contact.strip()}: {message.strip()}",
                context={"platform": "telegram", "contact": contact.strip()}
            )
            continue

        if cmd in ("check telegram", "telegram unread"):
            from execution.visual_agent import run_visual_goal
            run_visual_goal("check telegram unread messages",
                            context={"platform": "telegram"})
            continue

        # -------------------------
        # PERMISSIONS
        # -------------------------
        if cmd in ("permissions", "show permissions"):
            from core.permission_system import show_permissions
            show_permissions()
            continue

        if cmd.startswith("fury permission grant "):
            from core.permission_system import grant_permission
            grant_permission(cmd.replace("fury permission grant ", "").strip())
            continue

        if cmd.startswith("fury permission deny "):
            from core.permission_system import deny_permission
            deny_permission(cmd.replace("fury permission deny ", "").strip())
            continue

        if cmd == "fury permission reset":
            from core.permission_system import reset_permissions
            reset_permissions()
            continue

        # -------------------------
        # DEBUG
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
            final_core.what_do_i_know(cmd.replace("fury knows ", "").strip())
            continue

        if cmd == "fury help":
            print("""
=== FURY COMMANDS ===
exit / voice mode / text mode

--- VISUAL AGENT ---
visual <goal>           e.g. visual play lofi on youtube
resume / visual history
decompose <goal>

--- LEETCODE ---
leetcode <problem>      e.g. leetcode two sum

--- JOB SEARCH (read only — safe) ---
search jobs <role> <platform>
  e.g. search jobs react developer naukri
  e.g. search jobs mern developer indeed
read job <url>
write cover letter <role> <company>
draft email <hr@email.com> <role> <company>

--- MESSAGING ---
whatsapp <contact> <message>
read whatsapp <contact>
check whatsapp
telegram <contact> <message>
check telegram

--- GMAIL ---
check email
compose email to <email> about <what to say>

--- PROFILE ---
profile / fury profile reload

--- TABS ---
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