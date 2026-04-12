

# import time

# from agents.agent_controller import controller
# from core.self_improve import self_improve
# from memory.session_db import session_db
# from memory.experience_memory import save_experience, load_experiences
# from brain.pattern_engine import get_frequent_command
# from execution.task_planner import create_plan
# from execution.workflow_engine import run_workflow
# from brain.context_engine import enrich_command
# from brain.personality import respond

# # STEP 111
# from core.thinking_engine_v2 import think, is_vague

# # STEP 113
# from brain.reflection_engine import reflect

# # STEP 115
# from brain.curiosity_engine import should_ask

# # STEP 117
# from memory.episodic_memory import save_episode, print_stats

# # STEP 118
# from memory.knowledge_graph import learn_from_execution, what_does_fury_know_about

# # STEP 119
# from brain.pattern_recognizer import print_pattern_report, get_failure_commands

# # STEP 120
# from brain.intent_predictor import print_suggestions


# PATTERN_REPORT_EVERY = 10


# class FinalCore:

#     def __init__(self):
#         self._last_command  = None
#         self._last_plan     = None
#         self._last_verdict  = None
#         self._exec_count    = 0

#     def execute(self, command):

#         print(respond("executing"))

#         # STEP 107 — enrich vague commands
#         command = enrich_command(command)

#         # STEP 111 — chain-of-thought reasoning
#         thought = think(command)

#         # STEP 115 — ask if key info is missing
#         question = should_ask(command, thought)

#         if question:
#             print(f"\nFury: {question}")
#             clarification = input(">>> ").strip()
#             if clarification:
#                 command = f"{command} {clarification}"
#                 command = enrich_command(command)
#                 thought = think(command)

#         # STEP 1 — build plan
#         plan = create_plan(command)
#         print(f"FinalCore → plan type: {type(plan)}")

#         # store for after_step
#         self._last_command = command
#         self._last_plan    = plan
#         self._last_verdict = None

#         # STEP 117 — start timer
#         start_ms = int(time.time() * 1000)

#         # STEP 2 — execute
#         if isinstance(plan, dict) and "workflow" in plan:
#             print("FinalCore → running workflow directly")
#             run_workflow(plan["workflow"])
#         else:
#             controller.execute(plan)

#         duration_ms = int(time.time() * 1000) - start_ms

#         # STEP 3 — save experience (existing)
#         try:
#             save_experience(command, plan, result=True)
#         except Exception as e:
#             print("Experience save failed:", e)

#         print(respond("learn"))
#         self.after_step()

#         # STEP 117 — save full episode
#         try:
#             save_episode(
#                 command=command,
#                 plan=plan,
#                 outcome=self._last_verdict or "success",
#                 verdict=self._last_verdict,
#                 duration_ms=duration_ms
#             )
#         except Exception as e:
#             print(f"Episode save error: {e}")

#         print(respond("done"))

#         # STEP 120 — show next command suggestions
#         try:
#             print_suggestions(last_command=command)
#         except Exception as e:
#             pass

#         # periodic pattern report
#         self._exec_count += 1
#         try:
#             patterns = get_frequent_command()
#             if patterns:
#                 print("📊 Frequent actions:", patterns[:2])

#             if self._exec_count % PATTERN_REPORT_EVERY == 0:
#                 print("\n🔍 Running pattern analysis...")
#                 print_pattern_report()
#         except:
#             pass

#     def after_step(self):

#         self_improve.improve()

#         # STEP 113 — reflect
#         try:
#             reflection = reflect(self._last_command, self._last_plan)
#             if reflection:
#                 self._last_verdict = reflection.get("verdict")
#         except Exception as e:
#             print(f"Reflection error: {e}")

#         # STEP 118 — knowledge graph
#         try:
#             learn_from_execution(
#                 command=self._last_command,
#                 plan=self._last_plan,
#                 outcome=self._last_verdict or "success"
#             )
#         except Exception as e:
#             print(f"Knowledge graph error: {e}")

#     def save_state(self):
#         session_db.save("last", "ok")

#     def show_stats(self):
#         print_stats()

#     def what_do_i_know(self, concept):
#         what_does_fury_know_about(concept)

#     def show_patterns(self):
#         print_pattern_report()

#     def show_failures(self):
#         failures = get_failure_commands()
#         print("\n--- Commands that need fixing ---")
#         for f in failures:
#             print(f"  '{f['command']}' — {f['reason']}")
#         print()


# final_core = FinalCore()




# core/final_core.py
# STEP 111 — thinking_engine_v2
# STEP 112 — planner_v2 (inside task_planner)
# STEP 113 — reflection_engine
# STEP 114 — vision_understanding (available to agents)
# STEP 115 — curiosity_engine
# STEP 116 — confidence_engine (inside agent_controller)
# STEP 117 — episodic_memory
# STEP 118 — knowledge_graph
# STEP 119 — pattern_recognizer
# STEP 120 — intent_predictor
# STEP 122 — config_loader
# STEP 125 — safety_sandbox

import time

from agents.agent_controller import controller
from core.self_improve import self_improve
from memory.session_db import session_db
from memory.experience_memory import save_experience
from brain.pattern_engine import get_frequent_command
from execution.task_planner import create_plan
from execution.workflow_engine import run_workflow
from brain.context_engine import enrich_command
from brain.personality import respond

from core.thinking_engine_v2 import think, is_vague
from brain.reflection_engine import reflect
from brain.curiosity_engine import should_ask
from memory.episodic_memory import save_episode, print_stats
from memory.knowledge_graph import learn_from_execution, what_does_fury_know_about
from brain.pattern_recognizer import print_pattern_report, get_failure_commands
from brain.intent_predictor import print_suggestions
from core.config_loader import cfg

# STEP 125
from core.safety_sandbox import check_command, sandbox_is_on

PATTERN_REPORT_EVERY = 10


class FinalCore:

    def __init__(self):
        self._last_command  = None
        self._last_plan     = None
        self._last_verdict  = None
        self._exec_count    = 0

    def execute(self, command):

        print(respond("executing"))

        # STEP 125 — raw command safety check before anything else
        blocked, reason = check_command(command)
        if blocked:
            print(f"\n🛡️  Fury: Cannot run this — {reason}")
            print("If you think this is a mistake, update safety.blocked_commands in config.yaml")
            return

        if sandbox_is_on():
            print("🛡️  Sandbox mode is ON — destructive actions are disabled")

        # STEP 107 — enrich vague commands
        command = enrich_command(command)

        # STEP 111 — chain-of-thought reasoning
        thought = think(command)

        # STEP 115 — ask if key info is missing
        question = should_ask(command, thought)

        if question:
            print(f"\nFury: {question}")
            clarification = input(">>> ").strip()
            if clarification:
                command = f"{command} {clarification}"
                command = enrich_command(command)
                thought = think(command)

        # STEP 1 — build plan
        plan = create_plan(command)
        print(f"FinalCore → plan type: {type(plan)}")

        self._last_command = command
        self._last_plan    = plan
        self._last_verdict = None

        start_ms = int(time.time() * 1000)

        # STEP 2 — execute
        # workflow_engine now has per-step safety checks (Step 125)
        if isinstance(plan, dict) and "workflow" in plan:
            print("FinalCore → running workflow directly")
            run_workflow(plan["workflow"])
        else:
            controller.execute(plan)

        duration_ms = int(time.time() * 1000) - start_ms

        try:
            save_experience(command, plan, result=True)
        except Exception as e:
            print("Experience save failed:", e)

        print(respond("learn"))
        self.after_step()

        try:
            save_episode(
                command=command,
                plan=plan,
                outcome=self._last_verdict or "success",
                verdict=self._last_verdict,
                duration_ms=duration_ms
            )
        except Exception as e:
            print(f"Episode save error: {e}")

        print(respond("done"))

        if cfg.ui.show_suggestions:
            try:
                print_suggestions(last_command=command)
            except:
                pass

        self._exec_count += 1
        try:
            patterns = get_frequent_command()
            if patterns:
                print("📊 Frequent actions:", patterns[:2])
            report_every = getattr(cfg.memory, "pattern_report_every", 10)
            if self._exec_count % report_every == 0:
                print_pattern_report()
        except:
            pass

    def after_step(self):
        self_improve.improve()
        try:
            reflection = reflect(self._last_command, self._last_plan)
            if reflection:
                self._last_verdict = reflection.get("verdict")
        except Exception as e:
            print(f"Reflection error: {e}")
        try:
            learn_from_execution(
                command=self._last_command,
                plan=self._last_plan,
                outcome=self._last_verdict or "success"
            )
        except Exception as e:
            print(f"Knowledge graph error: {e}")

    def save_state(self):
        session_db.save("last", "ok")

    def show_stats(self):
        print_stats()

    def what_do_i_know(self, concept):
        what_does_fury_know_about(concept)

    def show_patterns(self):
        print_pattern_report()

    def show_failures(self):
        failures = get_failure_commands()
        print("\n--- Commands that need fixing ---")
        for f in failures:
            print(f"  '{f['command']}' — {f['reason']}")
        print()


final_core = FinalCore()