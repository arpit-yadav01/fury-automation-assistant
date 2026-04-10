# execution/planner_v2.py
# STEP 112 — Multi-hypothesis planning
#
# When the normal parser fails or returns unknown,
# this generates 2-3 candidate plans and picks the best one.
#
# Plugs into task_planner.py:create_plan() as a fallback
# BEFORE the final [{"intent": "unknown"}] return.
#
# Output is always workflow-compatible:
# {"workflow": [...steps...]}

import os
import json
import re
from openai import OpenAI

# -------------------------
# SAME CLIENT AS llm_brain.py
# -------------------------

GROQ_KEY = os.getenv("GROQ_API_KEY")

client = None
if GROQ_KEY:
    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

# -------------------------
# KNOWN ACTIONS (must match workflow_engine.py)
# -------------------------

VALID_ACTIONS = {
    "open_app", "open_url", "type", "press",
    "hotkey", "click", "create_file", "terminal", "skill"
}

VALID_INTENTS = {
    "open_app", "open_website", "web_search", "create_file",
    "write_file", "type_text", "write_code", "run_terminal",
    "click_text", "open_vscode", "create_code_file",
    "write_code_dev", "save_file", "run_python", "run_dev_command"
}

# -------------------------
# PROMPT
# -------------------------

SYSTEM_PROMPT = """You are Fury's planning engine running on Windows.
A user gave a command. Generate exactly 3 different plans to accomplish it.
Return ONLY a JSON object. No explanation. No markdown. No backticks.

Format:
{
  "hypotheses": [
    {
      "confidence": 0.95,
      "reasoning": "one sentence why this plan works",
      "workflow": [
        {"action": "open_app", "name": "notepad"},
        {"action": "type", "text": "hello world"}
      ]
    },
    {
      "confidence": 0.70,
      "reasoning": "...",
      "workflow": [...]
    },
    {
      "confidence": 0.40,
      "reasoning": "...",
      "workflow": [...]
    }
  ]
}

Valid workflow actions:
- {"action": "open_app", "name": "<app name>"}
- {"action": "open_url", "url": "<full url>"}
- {"action": "type", "text": "<text to type>"}
- {"action": "create_file", "path": "<filename>"}
- {"action": "terminal", "cmd": "<terminal command>"}
- {"action": "skill", "data": {"intent": "<intent>", ...fields}}
- {"action": "press", "key": "<key>"}

Valid skill intents: open_app, open_website, web_search, create_file,
write_file, type_text, write_code, run_terminal, click_text

Rules:
- confidence is a float 0.0 to 1.0
- hypotheses must be sorted highest confidence first
- keep workflows short — 1 to 4 steps maximum
- use open_app for desktop apps (notepad, vscode, chrome, etc.)
- use open_url for websites
- be concrete — no placeholder values
"""

# -------------------------
# MAIN FUNCTION
# -------------------------

def multi_plan(command):
    """
    Generate 2-3 candidate plans for a command and return the best one.

    Returns a workflow dict: {"workflow": [...steps...]}
    or None if planning fails.
    """

    if not command or not isinstance(command, str):
        return None

    if client is None:
        print("PlannerV2: no LLM client")
        return None

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": command}
            ],
            temperature=0.4,
            max_tokens=600
        )

        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"```json", "", raw)
        raw = re.sub(r"```", "", raw)

        data = json.loads(raw)
        hypotheses = data.get("hypotheses", [])

        if not hypotheses:
            return None

        # sort by confidence descending (LLM should already do this)
        hypotheses.sort(key=lambda h: h.get("confidence", 0), reverse=True)

        _print_hypotheses(command, hypotheses)

        # pick best valid plan
        for h in hypotheses:
            workflow = h.get("workflow", [])
            if _is_valid_workflow(workflow):
                print(f"PlannerV2: selected plan (confidence {h.get('confidence')})")
                print(f"PlannerV2: reasoning — {h.get('reasoning')}")
                return {"workflow": workflow}

        # fallback: return best even if not perfectly valid
        best = hypotheses[0].get("workflow", [])
        if best:
            print("PlannerV2: using best available plan")
            return {"workflow": best}

        return None

    except Exception as e:
        print(f"PlannerV2 error: {e}")
        return None


# -------------------------
# VALIDATION
# -------------------------

def _is_valid_workflow(workflow):
    """Check that workflow steps use known actions."""
    if not workflow or not isinstance(workflow, list):
        return False
    for step in workflow:
        if not isinstance(step, dict):
            return False
        action = step.get("action")
        if action not in VALID_ACTIONS:
            return False
        # skill steps need a data.intent
        if action == "skill":
            intent = step.get("data", {}).get("intent")
            if intent not in VALID_INTENTS:
                return False
    return True


# -------------------------
# DEBUG PRINT
# -------------------------

def _print_hypotheses(command, hypotheses):
    print(f"\n--- PlannerV2: {len(hypotheses)} hypotheses for: '{command}' ---")
    for i, h in enumerate(hypotheses):
        print(f"  [{i+1}] confidence={h.get('confidence')} — {h.get('reasoning')}")
    print("---\n")