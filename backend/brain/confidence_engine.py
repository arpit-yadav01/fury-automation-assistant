# brain/confidence_engine.py
# STEP 116 — Confidence scoring
#
# Before any agent handles a task, score how confident Fury is.
# Low confidence → ask before acting (not after failing).
#
# Three layers:
#   1. Rule-based fast score (no LLM) — based on intent + task completeness
#   2. LLM score — for complex or ambiguous tasks
#   3. Decision — proceed / ask / abort based on score
#
# Plugs into agent_controller.py before agent.handle(task)

import os
import json
import re
from openai import OpenAI

# -------------------------
# CLIENT
# -------------------------

GROQ_KEY = os.getenv("GROQ_API_KEY")

client = None
if GROQ_KEY:
    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

# -------------------------
# THRESHOLDS
# -------------------------

CONFIDENCE_HIGH   = 0.75   # proceed without asking
CONFIDENCE_LOW    = 0.40   # ask before acting
                           # below 0.40 → abort with explanation

# -------------------------
# REQUIRED FIELDS PER INTENT
# -------------------------

REQUIRED_FIELDS = {
    "open_app":      ["app"],
    "open_website":  ["url"],
    "web_search":    ["query"],
    "create_file":   ["filename"],
    "write_file":    ["filename", "text"],
    "type_text":     ["text"],
    "write_code":    ["task"],
    "run_terminal":  ["command"],
    "click_text":    ["text"],
    "run_python":    ["filename"],
}

# -------------------------
# FAST RULE-BASED SCORE
# -------------------------

def _rule_score(task):
    """
    Score 0.0–1.0 based on intent + required fields present.
    No LLM needed — runs instantly.
    """
    if not isinstance(task, dict):
        return 0.1

    intent = task.get("intent")

    if not intent or intent == "unknown":
        return 0.0

    required = REQUIRED_FIELDS.get(intent, [])

    if not required:
        # intent known but no required fields defined — moderate confidence
        return 0.65

    present = sum(1 for f in required if task.get(f))
    score = present / len(required)

    # boost if raw command is also present
    if task.get("raw"):
        score = min(score + 0.1, 1.0)

    return round(score, 2)


# -------------------------
# LLM SCORE (for complex tasks)
# -------------------------

SCORE_PROMPT = """You are Fury's confidence engine.
Given a task dict, score how confident Fury should be executing it.

Return ONLY a JSON object. No explanation. No markdown. No backticks.

Format:
{
  "score": 0.85,
  "reason": "<one sentence why>",
  "risky": true or false
}

Rules:
- score is 0.0 to 1.0
- risky = true if task could delete files, send emails, run dangerous commands
- score above 0.75 = proceed confidently
- score 0.40–0.75 = proceed with caution or ask first
- score below 0.40 = ask user before doing anything
"""

def _llm_score(task):
    if client is None:
        return None
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SCORE_PROMPT},
                {"role": "user", "content": json.dumps(task)}
            ],
            temperature=0.1,
            max_tokens=100
        )
        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"```json", "", raw)
        raw = re.sub(r"```", "", raw)
        return json.loads(raw)
    except Exception as e:
        print(f"ConfidenceEngine LLM error: {e}")
        return None


# -------------------------
# RISKY INTENT DETECTOR
# -------------------------

RISKY_INTENTS = {
    "run_terminal", "delete_file", "write_file",
    "send_email", "run_python"
}

def _is_risky(task):
    intent = task.get("intent", "") if isinstance(task, dict) else ""
    if intent in RISKY_INTENTS:
        return True
    # check for dangerous terminal commands
    cmd = task.get("command", "").lower() if isinstance(task, dict) else ""
    dangerous = ["rm ", "del ", "format", "shutdown", "rmdir", ":(){"]
    return any(d in cmd for d in dangerous)


# -------------------------
# MAIN FUNCTION
# -------------------------

def score_task(task):
    """
    Score confidence for a task.

    Returns:
    {
        "score": float,        # 0.0 to 1.0
        "decision": str,       # "proceed" | "ask" | "abort"
        "reason": str,
        "risky": bool
    }
    """

    # fast rule score
    rule = _rule_score(task)
    risky = _is_risky(task)

    # for risky or borderline tasks, use LLM score
    use_llm = risky or (CONFIDENCE_LOW <= rule <= CONFIDENCE_HIGH)

    llm_result = None
    if use_llm:
        llm_result = _llm_score(task)

    # final score — average if both available
    if llm_result and isinstance(llm_result.get("score"), (int, float)):
        final_score = round((rule + llm_result["score"]) / 2, 2)
        reason = llm_result.get("reason", "")
        risky = risky or llm_result.get("risky", False)
    else:
        final_score = rule
        reason = _rule_reason(task, rule)

    # decision
    if risky and final_score < CONFIDENCE_HIGH:
        decision = "ask"
    elif final_score >= CONFIDENCE_HIGH:
        decision = "proceed"
    elif final_score >= CONFIDENCE_LOW:
        decision = "ask"
    else:
        decision = "abort"

    result = {
        "score": final_score,
        "decision": decision,
        "reason": reason,
        "risky": risky
    }

    _print_score(task, result)
    return result


def _rule_reason(task, score):
    intent = task.get("intent", "unknown") if isinstance(task, dict) else "unknown"
    if score == 0.0:
        return f"Intent '{intent}' is unknown"
    if score < CONFIDENCE_LOW:
        return f"Missing required fields for intent '{intent}'"
    if score < CONFIDENCE_HIGH:
        return f"Partial info for intent '{intent}'"
    return f"All required fields present for '{intent}'"


def _print_score(task, result):
    intent = task.get("intent", "?") if isinstance(task, dict) else "?"
    print(f"Confidence [{intent}]: {result['score']} → {result['decision']}", end="")
    if result["risky"]:
        print(" ⚠️ risky", end="")
    print()