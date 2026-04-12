# brain/intent_predictor.py
# STEP 120 — Intent predictor
#
# Predicts what the user is likely to do next based on:
#   1. Sequence patterns — what usually follows the last command
#   2. Current context  — what app/site is active right now
#   3. Time patterns    — what commands happen at similar times
#   4. Frequency        — what commands are run most overall
#
# Used by:
#   - fury.py → show suggestions after each command
#   - curiosity_engine.py → smarter clarification using predicted intent
#   - final_core.py → proactive suggestions

from collections import defaultdict, Counter
from datetime import datetime

from memory.experience_memory import load_experiences
from brain.context_memory import memory as ctx


# -------------------------
# SEQUENCE TABLE BUILDER
# -------------------------

def _build_sequence_table(experiences):
    """
    Build a table: given command A, what commands usually follow?
    Returns: { command_a: Counter({command_b: count}) }
    """
    table = defaultdict(Counter)
    cmds = [exp["command"] for exp in experiences]

    for i in range(len(cmds) - 1):
        table[cmds[i]][cmds[i + 1]] += 1

    return table


# -------------------------
# CONTEXT SCORE
# -------------------------

def _context_score(command, cur_app, cur_site):
    """
    Score a candidate command based on how well it fits current context.
    """
    cmd = command.lower()
    score = 0.0

    if cur_app == "browser":
        if "search" in cmd or "open" in cmd or "youtube" in cmd or "google" in cmd:
            score += 0.3

    if cur_site == "youtube":
        if "youtube" in cmd or "search" in cmd or "play" in cmd:
            score += 0.4

    if cur_site == "google":
        if "google" in cmd or "search" in cmd:
            score += 0.3

    if cur_app == "notepad":
        if "type" in cmd or "write" in cmd:
            score += 0.4

    if cur_app == "vscode" or cur_app == "code":
        if "create" in cmd or "write" in cmd or "run" in cmd or ".py" in cmd:
            score += 0.4

    return score


# -------------------------
# TIME SCORE
# -------------------------

def _time_score(experiences, command):
    """
    Score a command based on how often it was run at a similar hour.
    """
    current_hour = datetime.now().hour
    score = 0.0
    count = 0

    for exp in experiences:
        if exp["command"] != command:
            continue
        ts = exp.get("timestamp", "")
        try:
            hour = datetime.fromisoformat(ts).hour
            if abs(hour - current_hour) <= 2:
                score += 1.0
            count += 1
        except:
            continue

    return score / max(count, 1)


# -------------------------
# MAIN PREDICTION
# -------------------------

def predict_next(last_command=None, top_n=3):
    """
    Predict the top N most likely next commands.

    Args:
        last_command: the command just executed (optional)
        top_n: how many predictions to return

    Returns:
        list of dicts: [{"command": str, "score": float, "reason": str}]
    """
    experiences = load_experiences()

    if not experiences:
        return []

    cur_app  = ctx.get_app()  or ""
    cur_site = ctx.get_site() or ""

    candidates = {}  # command → score

    # --- Layer 1: sequence following ---
    if last_command:
        seq_table = _build_sequence_table(experiences)
        followers = seq_table.get(last_command.lower().strip(), Counter())
        total_follows = sum(followers.values()) or 1
        for cmd, count in followers.most_common(10):
            seq_score = count / total_follows
            candidates[cmd] = candidates.get(cmd, 0.0) + seq_score * 0.5

    # --- Layer 2: frequency ---
    freq = Counter(exp["command"] for exp in experiences)
    total_freq = sum(freq.values()) or 1
    for cmd, count in freq.most_common(10):
        freq_score = count / total_freq
        candidates[cmd] = candidates.get(cmd, 0.0) + freq_score * 0.3

    # --- Layer 3: context ---
    for cmd in list(candidates.keys()):
        ctx_score = _context_score(cmd, cur_app, cur_site)
        candidates[cmd] += ctx_score * 0.15

    # --- Layer 4: time ---
    for cmd in list(candidates.keys()):
        t_score = _time_score(experiences, cmd)
        candidates[cmd] += t_score * 0.05

    # skip last command itself
    if last_command:
        candidates.pop(last_command.lower().strip(), None)

    # sort and build result
    sorted_candidates = sorted(
        candidates.items(), key=lambda x: -x[1]
    )[:top_n]

    result = []
    for cmd, score in sorted_candidates:
        result.append({
            "command": cmd,
            "score": round(score, 3),
            "reason": _explain(cmd, last_command, cur_app, cur_site)
        })

    return result


# -------------------------
# EXPLAIN PREDICTION
# -------------------------

def _explain(command, last_command, cur_app, cur_site):
    """One-sentence reason for the prediction."""
    cmd = command.lower()

    if last_command and _commands_often_follow(last_command, command):
        return f"often runs after '{last_command}'"

    if cur_site and cur_site in cmd:
        return f"matches current site ({cur_site})"

    if cur_app and cur_app in cmd:
        return f"matches current app ({cur_app})"

    return "frequently used command"


def _commands_often_follow(a, b):
    """Quick check if b often follows a in history."""
    experiences = load_experiences()
    seq_table = _build_sequence_table(experiences)
    followers = seq_table.get(a.lower().strip(), Counter())
    return followers.get(b.lower().strip(), 0) >= 2


# -------------------------
# PRINT SUGGESTIONS
# -------------------------

def print_suggestions(last_command=None):
    predictions = predict_next(last_command=last_command, top_n=3)

    if not predictions:
        return

    print("\n💡 Fury suggests:")
    for i, p in enumerate(predictions, 1):
        print(f"   {i}. '{p['command']}' — {p['reason']}")
    print()


# -------------------------
# GET TOP PREDICTED INTENT
# -------------------------

def get_predicted_intent(last_command=None):
    """
    Returns just the single most likely next command string.
    Used by curiosity_engine and other modules.
    """
    predictions = predict_next(last_command=last_command, top_n=1)
    if predictions:
        return predictions[0]["command"]
    return None