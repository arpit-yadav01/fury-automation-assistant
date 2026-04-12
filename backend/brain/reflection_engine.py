# # brain/reflection_engine.py
# # STEP 113 — Self-reflection engine
# #
# # After every execution, Fury reviews:
# #   - the last command and its plan
# #   - any failures that happened during it
# #   - patterns across recent history
# #
# # Produces a short critique saved to memory/reflections.json
# # Plugs into final_core.py → after_step()

# import os
# import json
# import re
# from datetime import datetime
# from openai import OpenAI

# from memory.experience_memory import load_experiences
# from brain.failure_memory import get_failures

# # -------------------------
# # SAME CLIENT AS llm_brain.py
# # -------------------------

# GROQ_KEY = os.getenv("GROQ_API_KEY")

# client = None
# if GROQ_KEY:
#     client = OpenAI(
#         api_key=GROQ_KEY,
#         base_url="https://api.groq.com/openai/v1"
#     )

# # -------------------------
# # REFLECTION STORE
# # -------------------------

# REFLECTION_FILE = "memory/reflections.json"


# def _init():
#     if not os.path.exists("memory"):
#         os.makedirs("memory")
#     if not os.path.exists(REFLECTION_FILE):
#         with open(REFLECTION_FILE, "w") as f:
#             json.dump([], f)


# def save_reflection(reflection: dict):
#     _init()
#     try:
#         with open(REFLECTION_FILE, "r") as f:
#             data = json.load(f)
#         data.append(reflection)
#         # keep last 100 reflections only
#         data = data[-100:]
#         with open(REFLECTION_FILE, "w") as f:
#             json.dump(data, f, indent=2)
#     except Exception as e:
#         print(f"Reflection save error: {e}")


# def load_reflections():
#     _init()
#     try:
#         with open(REFLECTION_FILE, "r") as f:
#             return json.load(f)
#     except:
#         return []


# def get_last_reflection():
#     reflections = load_reflections()
#     return reflections[-1] if reflections else None


# # -------------------------
# # PROMPT
# # -------------------------

# SYSTEM_PROMPT = """You are Fury's self-reflection engine.
# You review what just happened and produce a short honest critique.

# You will receive:
# - last_command: the command Fury just executed
# - last_plan: the workflow plan that was built
# - recent_failures: any steps that failed during execution
# - recent_history: last 5 commands Fury ran

# Return ONLY a JSON object. No explanation. No markdown. No backticks.

# Format:
# {
#   "verdict": "success" | "partial" | "failure",
#   "what_worked": "<one sentence>",
#   "what_failed": "<one sentence or null>",
#   "root_cause": "<why it failed, or null if success>",
#   "improvement": "<one concrete suggestion for next time, or null>"
# }

# Rules:
# - Be honest and specific — not generic
# - what_failed and root_cause are null if verdict is success
# - improvement should be actionable — something Fury can actually do differently
# - Keep every field to one sentence maximum
# """


# # -------------------------
# # MAIN FUNCTION
# # -------------------------

# def reflect(command, plan, failures=None):
#     """
#     Reflect on the last execution.

#     Args:
#         command: the command that was executed
#         plan: the plan that was built and run
#         failures: list of failure dicts from this execution (optional)

#     Returns:
#         reflection dict, also saved to memory/reflections.json
#     """

#     if not command:
#         return None

#     # build context for LLM
#     recent = _get_recent_history(n=5, exclude=command)
#     recent_failures = failures or _get_recent_failures(n=5)

#     context = {
#         "last_command": command,
#         "last_plan": _summarize_plan(plan),
#         "recent_failures": recent_failures,
#         "recent_history": recent,
#     }

#     # local reflection if no LLM
#     if client is None:
#         return _local_reflect(command, plan, recent_failures)

#     try:
#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {"role": "system", "content": SYSTEM_PROMPT},
#                 {"role": "user", "content": json.dumps(context)}
#             ],
#             temperature=0.2,
#             max_tokens=250
#         )

#         raw = response.choices[0].message.content.strip()
#         raw = re.sub(r"```json", "", raw)
#         raw = re.sub(r"```", "", raw)

#         reflection = json.loads(raw)
#         reflection["command"] = command
#         reflection["timestamp"] = str(datetime.now())

#         _print_reflection(reflection)
#         save_reflection(reflection)
#         return reflection

#     except Exception as e:
#         print(f"ReflectionEngine error: {e}")
#         return _local_reflect(command, plan, recent_failures)


# # -------------------------
# # LOCAL FALLBACK (no LLM)
# # -------------------------

# def _local_reflect(command, plan, failures):
#     """Simple rule-based reflection when LLM is unavailable."""

#     has_failures = bool(failures)
#     has_plan = bool(plan) and plan != [{"intent": "unknown"}]

#     if not has_plan:
#         verdict = "failure"
#         what_worked = "Command was received"
#         what_failed = "No valid plan could be built"
#         root_cause = "Command not understood by any parser"
#         improvement = "Add this command pattern to command_parser.py"
#     elif has_failures:
#         verdict = "partial"
#         what_worked = "Plan was built and partially executed"
#         what_failed = f"{len(failures)} step(s) failed during execution"
#         root_cause = failures[0].get("error", "unknown") if failures else None
#         improvement = "Check skill implementation for failed intent"
#     else:
#         verdict = "success"
#         what_worked = "Command executed successfully"
#         what_failed = None
#         root_cause = None
#         improvement = None

#     reflection = {
#         "command": command,
#         "verdict": verdict,
#         "what_worked": what_worked,
#         "what_failed": what_failed,
#         "root_cause": root_cause,
#         "improvement": improvement,
#         "timestamp": str(datetime.now())
#     }

#     _print_reflection(reflection)
#     save_reflection(reflection)
#     return reflection


# # -------------------------
# # HELPERS
# # -------------------------

# def _get_recent_history(n=5, exclude=None):
#     """Get last n commands from experience memory."""
#     experiences = load_experiences()
#     history = []
#     for exp in reversed(experiences):
#         cmd = exp.get("command", "")
#         if cmd == exclude:
#             continue
#         history.append(cmd)
#         if len(history) >= n:
#             break
#     return history


# def _get_recent_failures(n=5):
#     """Get last n failures from failure memory."""
#     failures = get_failures()
#     return failures[-n:] if failures else []


# def _summarize_plan(plan):
#     """Produce a short readable summary of a plan."""
#     if not plan:
#         return "no plan"
#     if isinstance(plan, list):
#         intents = [p.get("intent", "?") for p in plan if isinstance(p, dict)]
#         return f"list: {intents}"
#     if isinstance(plan, dict) and "workflow" in plan:
#         actions = [s.get("action", "?") for s in plan["workflow"]]
#         return f"workflow: {actions}"
#     return str(plan)[:80]


# def _print_reflection(r):
#     print("\n--- Fury Reflecting ---")
#     print(f"Verdict     : {r.get('verdict')}")
#     print(f"What worked : {r.get('what_worked')}")
#     if r.get("what_failed"):
#         print(f"What failed : {r.get('what_failed')}")
#     if r.get("root_cause"):
#         print(f"Root cause  : {r.get('root_cause')}")
#     if r.get("improvement"):
#         print(f"Improve     : {r.get('improvement')}")
#     print("-----------------------\n")



# brain/reflection_engine.py
# STEP 113 — Self-reflection engine
# FIX: _is_bad_plan now correctly reads write_code skill steps as success

import os
import json
import re
from datetime import datetime
from openai import OpenAI

from memory.experience_memory import load_experiences
from brain.failure_memory import get_failures

GROQ_KEY = os.getenv("GROQ_API_KEY")
client = None
if GROQ_KEY:
    client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")

# ✅ FIX: path relative to this file
_DIR = os.path.dirname(os.path.abspath(__file__))
REFLECTION_FILE = os.path.join(os.path.dirname(_DIR), "memory", "reflections.json")


def _init():
    os.makedirs(os.path.dirname(REFLECTION_FILE), exist_ok=True)
    if not os.path.exists(REFLECTION_FILE):
        with open(REFLECTION_FILE, "w") as f:
            json.dump([], f)


def save_reflection(reflection):
    _init()
    try:
        with open(REFLECTION_FILE, "r") as f:
            data = json.load(f)
        data.append(reflection)
        data = data[-100:]
        with open(REFLECTION_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Reflection save error: {e}")


def load_reflections():
    _init()
    try:
        with open(REFLECTION_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def get_last_reflection():
    reflections = load_reflections()
    return reflections[-1] if reflections else None


SYSTEM_PROMPT = """You are Fury's self-reflection engine.
You review what just happened and produce a short honest critique.

You will receive:
- last_command: the command Fury just executed
- last_plan: the workflow plan that was built
- recent_failures: any steps that failed during execution
- recent_history: last 5 commands Fury ran

Return ONLY a JSON object. No explanation. No markdown. No backticks.

Format:
{
  "verdict": "success" | "partial" | "failure",
  "what_worked": "<one sentence>",
  "what_failed": "<one sentence or null>",
  "root_cause": "<why it failed, or null if success>",
  "improvement": "<one concrete suggestion for next time, or null>"
}

Rules:
- verdict is "success" if the plan was executed and main goal was achieved
- verdict is "partial" if some steps worked but others failed
- verdict is "failure" only if the main goal completely failed
- A workflow with write_code + create_file that both ran = SUCCESS
- Be honest and specific — not generic
- Keep every field to one sentence maximum
"""


def reflect(command, plan, failures=None):
    if not command:
        return None

    recent = _get_recent_history(n=5, exclude=command)
    recent_failures = failures or _get_recent_failures(n=3)

    # ✅ FIX: check plan quality locally before calling LLM
    plan_quality = _assess_plan_quality(plan)

    context = {
        "last_command": command,
        "last_plan": _summarize_plan(plan),
        "plan_quality": plan_quality,
        "recent_failures": recent_failures,
        "recent_history": recent,
    }

    if client is None:
        return _local_reflect(command, plan, recent_failures)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(context)}
            ],
            temperature=0.2,
            max_tokens=250
        )

        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"```json", "", raw)
        raw = re.sub(r"```", "", raw)

        reflection = json.loads(raw)
        reflection["command"] = command
        reflection["timestamp"] = str(datetime.now())

        _print_reflection(reflection)
        save_reflection(reflection)
        return reflection

    except Exception as e:
        print(f"ReflectionEngine error: {e}")
        return _local_reflect(command, plan, recent_failures)


def _assess_plan_quality(plan):
    """
    ✅ FIX: correctly assess plan quality.
    A plan with write_code or create_file skills is GOOD — not unknown.
    Only flag as bad if ALL steps have intent:unknown.
    """
    if not plan:
        return "no_plan"

    if isinstance(plan, dict) and "workflow" in plan:
        steps = plan["workflow"]
        if not steps:
            return "empty_workflow"

        unknown_count = 0
        good_intents = {
            "write_code", "create_file", "open_app", "open_website",
            "web_search", "type_text", "run_terminal", "write_file"
        }

        for step in steps:
            if not isinstance(step, dict):
                continue
            action = step.get("action", "")
            if action == "skill":
                intent = step.get("data", {}).get("intent", "")
                if intent == "unknown":
                    unknown_count += 1
            elif action in ("open_url", "type", "create_file", "open_app"):
                pass  # these are always good

        # only bad if ALL skill steps are unknown
        total_steps = len(steps)
        if unknown_count == total_steps:
            return "all_unknown"
        if unknown_count > 0:
            return "partial_unknown"
        return "good"

    if isinstance(plan, list):
        all_unknown = all(
            isinstance(p, dict) and p.get("intent") == "unknown"
            for p in plan
        )
        return "all_unknown" if all_unknown else "good"

    return "good"


def _local_reflect(command, plan, failures):
    quality = _assess_plan_quality(plan)

    if quality in ("no_plan", "all_unknown"):
        verdict = "failure"
        what_worked = "Command was received"
        what_failed = "No valid plan could be built"
        root_cause = "Command not understood by any parser"
        improvement = "Add this command pattern to command_parser.py"
    elif quality == "partial_unknown":
        verdict = "partial"
        what_worked = "Some steps executed successfully"
        what_failed = "Some steps had unknown intent"
        root_cause = "Partial command parsing failure"
        improvement = "Improve parser coverage for this command pattern"
    elif failures:
        verdict = "partial"
        what_worked = "Plan was built and partially executed"
        what_failed = f"{len(failures)} step(s) failed during execution"
        root_cause = failures[0].get("error", "unknown") if failures else None
        improvement = "Check skill implementation for failed intent"
    else:
        verdict = "success"
        what_worked = "Command executed successfully"
        what_failed = None
        root_cause = None
        improvement = None

    reflection = {
        "command": command,
        "verdict": verdict,
        "what_worked": what_worked,
        "what_failed": what_failed,
        "root_cause": root_cause,
        "improvement": improvement,
        "timestamp": str(datetime.now())
    }

    _print_reflection(reflection)
    save_reflection(reflection)
    return reflection


def _get_recent_history(n=5, exclude=None):
    experiences = load_experiences()
    history = []
    for exp in reversed(experiences):
        cmd = exp.get("command", "")
        if cmd == exclude:
            continue
        history.append(cmd)
        if len(history) >= n:
            break
    return history


def _get_recent_failures(n=3):
    failures = get_failures()
    return failures[-n:] if failures else []


def _summarize_plan(plan):
    if not plan:
        return "no plan"
    if isinstance(plan, list):
        intents = [p.get("intent", "?") for p in plan if isinstance(p, dict)]
        return f"list: {intents}"
    if isinstance(plan, dict) and "workflow" in plan:
        actions = []
        for s in plan["workflow"]:
            if s.get("action") == "skill":
                actions.append(f"skill:{s.get('data',{}).get('intent','?')}")
            else:
                actions.append(s.get("action", "?"))
        return f"workflow: {actions}"
    return str(plan)[:80]


def _print_reflection(r):
    print("\n--- Fury Reflecting ---")
    print(f"Verdict     : {r.get('verdict')}")
    print(f"What worked : {r.get('what_worked')}")
    if r.get("what_failed"):
        print(f"What failed : {r.get('what_failed')}")
    if r.get("root_cause"):
        print(f"Root cause  : {r.get('root_cause')}")
    if r.get("improvement"):
        print(f"Improve     : {r.get('improvement')}")
    print("-----------------------\n")