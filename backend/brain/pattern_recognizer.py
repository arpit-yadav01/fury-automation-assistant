# brain/pattern_recognizer.py
# STEP 119 — Pattern recognizer
#
# Analyzes experience_memory.json to find:
#   1. Repeated exact commands (already in pattern_engine.py — we extend it)
#   2. Template patterns — "open youtube and search X", "create X.py and write Y"
#   3. Sequence patterns — commands that often follow each other
#   4. Failure patterns — commands that repeatedly produce unknown/bad plans
#   5. Time patterns — commands used at similar times
#
# Does NOT replace pattern_engine.py — adds richer analysis on top.
# Called from final_core.py and can be queried directly.

import re
from collections import defaultdict, Counter
from datetime import datetime

from memory.experience_memory import load_experiences


# -------------------------
# TEMPLATE PATTERNS
# Known command shapes — X and Y are variables
# -------------------------

TEMPLATES = [
    (r"^open (.+) and search (.+)$",        "open_and_search",   ["site", "query"]),
    (r"^create (.+\.py) and write (.+)$",    "create_and_code",   ["filename", "task"]),
    (r"^open (.+) and (type|write) (.+)$",   "open_and_type",     ["app", "verb", "text"]),
    (r"^search (.+) on (.+)$",               "search_on",         ["query", "site"]),
    (r"^open (.+) and (run|execute) (.+)$",  "open_and_run",      ["app", "verb", "cmd"]),
    (r"^pip install (.+)$",                  "pip_install",        ["package"]),
    (r"^create (.+) and write (.+)$",        "create_and_write",  ["filename", "content"]),
]


# -------------------------
# MAIN ANALYSIS
# -------------------------

def analyze_patterns():
    """
    Full pattern analysis over experience_memory.json.

    Returns:
    {
        "repeated":   [...],   # exact commands run 2+ times
        "templates":  [...],   # detected template patterns with variables
        "sequences":  [...],   # command pairs that often follow each other
        "failures":   [...],   # commands that produce bad/unknown plans
        "top_actions":[...],   # most common workflow actions
    }
    """
    experiences = load_experiences()

    if not experiences:
        return {}

    repeated   = _find_repeated(experiences)
    templates  = _find_templates(experiences)
    sequences  = _find_sequences(experiences)
    failures   = _find_failures(experiences)
    top_actions = _find_top_actions(experiences)

    result = {
        "repeated":    repeated,
        "templates":   templates,
        "sequences":   sequences,
        "failures":    failures,
        "top_actions": top_actions,
    }

    return result


# -------------------------
# 1. REPEATED COMMANDS
# -------------------------

def _find_repeated(experiences, min_count=2):
    counter = Counter(exp["command"] for exp in experiences)
    return [
        {"command": cmd, "count": count}
        for cmd, count in counter.most_common()
        if count >= min_count
    ]


# -------------------------
# 2. TEMPLATE PATTERNS
# -------------------------

def _find_templates(experiences):
    """
    Match commands against known templates and extract variables.
    Groups by template type and counts occurrences.
    """
    template_hits = defaultdict(list)

    for exp in experiences:
        cmd = exp["command"].lower().strip()
        for pattern, name, fields in TEMPLATES:
            m = re.match(pattern, cmd)
            if m:
                groups = m.groups()
                variables = dict(zip(fields, groups))
                template_hits[name].append({
                    "command": cmd,
                    "variables": variables,
                    "timestamp": exp.get("timestamp", "")
                })
                break

    result = []
    for name, hits in template_hits.items():
        if len(hits) >= 2:
            # extract unique variable values
            all_vars = defaultdict(set)
            for h in hits:
                for k, v in h["variables"].items():
                    all_vars[k].add(v)

            result.append({
                "template": name,
                "count": len(hits),
                "variable_values": {k: list(v) for k, v in all_vars.items()},
                "example": hits[0]["command"]
            })

    # sort by count
    result.sort(key=lambda x: -x["count"])
    return result


# -------------------------
# 3. SEQUENCE PATTERNS
# -------------------------

def _find_sequences(experiences, min_count=2):
    """
    Find pairs of commands that often run one after another.
    """
    pair_counter = Counter()
    cmds = [exp["command"] for exp in experiences]

    for i in range(len(cmds) - 1):
        pair = (cmds[i], cmds[i + 1])
        pair_counter[pair] += 1

    return [
        {"first": pair[0], "then": pair[1], "count": count}
        for pair, count in pair_counter.most_common(10)
        if count >= min_count
    ]


# -------------------------
# 4. FAILURE PATTERNS
# -------------------------

def _find_failures(experiences):
    """
    Find commands that produced unknown intents or bad plans.
    These are candidates for improvement.
    """
    failures = []

    for exp in experiences:
        plan = exp.get("plan")
        cmd  = exp.get("command", "")

        if _is_bad_plan(plan):
            failures.append({
                "command": cmd,
                "reason": _failure_reason(plan),
                "timestamp": exp.get("timestamp", "")
            })

    # deduplicate by command
    seen = set()
    unique = []
    for f in failures:
        if f["command"] not in seen:
            seen.add(f["command"])
            unique.append(f)

    return unique


def _is_bad_plan(plan):
    if not plan:
        return True
    if isinstance(plan, list):
        return all(
            isinstance(p, dict) and p.get("intent") == "unknown"
            for p in plan
        )
    if isinstance(plan, dict) and "workflow" in plan:
        steps = plan["workflow"]
        unknown_steps = [
            s for s in steps
            if isinstance(s, dict)
            and s.get("action") == "skill"
            and isinstance(s.get("data"), dict)
            and s["data"].get("intent") == "unknown"
        ]
        # bad if MORE than half the steps are unknown
        return len(unknown_steps) > len(steps) / 2
    return False


def _failure_reason(plan):
    if not plan:
        return "no plan built"
    if isinstance(plan, list):
        return "all intents unknown"
    if isinstance(plan, dict) and "workflow" in plan:
        return "workflow contains unknown steps"
    return "unrecognized plan format"


# -------------------------
# 5. TOP ACTIONS
# -------------------------

def _find_top_actions(experiences):
    """
    Count the most common workflow actions across all experiences.
    """
    action_counter = Counter()

    for exp in experiences:
        plan = exp.get("plan")
        if not isinstance(plan, dict) or "workflow" not in plan:
            continue
        for step in plan["workflow"]:
            if not isinstance(step, dict):
                continue
            action = step.get("action")
            if action == "skill":
                intent = step.get("data", {}).get("intent", "skill:unknown")
                action_counter[f"skill:{intent}"] += 1
            elif action:
                action_counter[action] += 1

    return [
        {"action": action, "count": count}
        for action, count in action_counter.most_common(10)
    ]


# -------------------------
# QUICK HELPERS
# -------------------------

def get_repeated_commands(threshold=2):
    """Shortcut — just repeated commands above threshold."""
    experiences = load_experiences()
    counter = Counter(exp["command"] for exp in experiences)
    return [
        (cmd, count)
        for cmd, count in counter.most_common()
        if count >= threshold
    ]


def get_failure_commands():
    """Shortcut — just commands that keep failing."""
    experiences = load_experiences()
    return _find_failures(experiences)


def get_template_summary():
    """Shortcut — just template patterns detected."""
    experiences = load_experiences()
    return _find_templates(experiences)


# -------------------------
# PRINT REPORT
# -------------------------

def print_pattern_report():
    patterns = analyze_patterns()

    print("\n====== FURY PATTERN REPORT ======")

    print("\n--- Repeated commands ---")
    for r in patterns.get("repeated", []):
        print(f"  [{r['count']}x] {r['command']}")

    print("\n--- Template patterns ---")
    for t in patterns.get("templates", []):
        print(f"  [{t['count']}x] {t['template']} — e.g. '{t['example']}'")
        for k, vals in t["variable_values"].items():
            print(f"       {k}: {vals}")

    print("\n--- Sequence patterns ---")
    for s in patterns.get("sequences", []):
        print(f"  [{s['count']}x] '{s['first']}' → '{s['then']}'")

    print("\n--- Failure patterns ---")
    for f in patterns.get("failures", []):
        print(f"  '{f['command']}' — {f['reason']}")

    print("\n--- Top actions ---")
    for a in patterns.get("top_actions", []):
        print(f"  [{a['count']}x] {a['action']}")

    print("=================================\n")