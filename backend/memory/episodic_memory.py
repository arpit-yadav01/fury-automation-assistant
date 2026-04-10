# memory/episodic_memory.py
# STEP 117 — Deep episodic memory
#
# Stores full episodes — not just command+plan but:
#   - full context at time of execution (app, window, site, file)
#   - outcome (success/partial/failure)
#   - reflection verdict
#   - duration
#   - similar past episodes at time of recall
#
# Uses fury.db (existing SQLite) — adds new table "episodes"
# Does NOT replace experience_memory.py — runs alongside it
#
# Key advantage over experience_memory:
#   find_similar_episode() matches by CONTEXT not just exact command text
#   so "open notepad" after using vscode recalls differently than cold start

import sqlite3
import os
import json
import time
from datetime import datetime

from brain.context_memory import memory as ctx

DB_PATH = os.path.join("memory", "fury.db")

# -------------------------
# DB SETUP
# -------------------------

def _get_conn():
    os.makedirs("memory", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    _create_table(conn)
    return conn


def _create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS episodes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            command     TEXT,
            intent      TEXT,
            context_app TEXT,
            context_win TEXT,
            context_site TEXT,
            context_file TEXT,
            plan        TEXT,
            outcome     TEXT,
            verdict     TEXT,
            duration_ms INTEGER,
            timestamp   TEXT
        )
    """)
    conn.commit()


# -------------------------
# SAVE EPISODE
# -------------------------

def save_episode(command, plan, outcome="success", verdict=None, duration_ms=0):
    """
    Save a full episode to SQLite.

    Args:
        command:     the command that was run
        plan:        the workflow dict or list
        outcome:     "success" | "partial" | "failure"
        verdict:     reflection verdict string (optional)
        duration_ms: how long execution took in ms
    """
    if not command:
        return

    # extract top-level intent from plan
    intent = _extract_intent(plan)

    # snapshot context at time of saving
    context_app  = ctx.get_app()  or ""
    context_win  = ctx.get_window() or ""
    context_site = ctx.get_site() or ""
    context_file = ctx.get_file() or ""

    plan_json = json.dumps(plan) if plan else ""
    timestamp = str(datetime.now())

    try:
        conn = _get_conn()
        conn.execute("""
            INSERT INTO episodes
            (command, intent, context_app, context_win, context_site,
             context_file, plan, outcome, verdict, duration_ms, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            command.lower().strip(),
            intent,
            context_app,
            context_win,
            context_site,
            context_file,
            plan_json,
            outcome,
            verdict or "",
            duration_ms,
            timestamp
        ))
        conn.commit()
        conn.close()
        print("📼 Episode saved")
    except Exception as e:
        print(f"Episodic memory save error: {e}")


# -------------------------
# RECALL — exact command
# -------------------------

def recall_command(command, limit=3):
    """
    Recall past episodes for an exact command.
    Returns list of episode dicts, most recent first.
    """
    try:
        conn = _get_conn()
        rows = conn.execute("""
            SELECT command, intent, context_app, context_win, context_site,
                   context_file, plan, outcome, verdict, duration_ms, timestamp
            FROM episodes
            WHERE command = ?
            ORDER BY id DESC LIMIT ?
        """, (command.lower().strip(), limit)).fetchall()
        conn.close()
        return [_row_to_dict(r) for r in rows]
    except Exception as e:
        print(f"Episodic recall error: {e}")
        return []


# -------------------------
# RECALL — similar context
# -------------------------

def find_similar_episode(command, limit=3):
    """
    Find episodes with similar command OR similar context.
    Scores each episode and returns best matches.

    This is the key upgrade over experience_memory.find_similar():
    matches on context (same app, same site) not just exact text.
    """
    try:
        conn = _get_conn()

        # current context for comparison
        cur_app  = ctx.get_app()  or ""
        cur_site = ctx.get_site() or ""
        cur_file = ctx.get_file() or ""

        # get recent episodes to score
        rows = conn.execute("""
            SELECT command, intent, context_app, context_win, context_site,
                   context_file, plan, outcome, verdict, duration_ms, timestamp
            FROM episodes
            ORDER BY id DESC LIMIT 50
        """).fetchall()
        conn.close()

        episodes = [_row_to_dict(r) for r in rows]
        scored = []

        cmd_lower = command.lower().strip()

        for ep in episodes:
            score = 0.0

            # exact command match — highest weight
            if ep["command"] == cmd_lower:
                score += 0.6

            # partial command match
            elif _words_overlap(cmd_lower, ep["command"]) >= 2:
                score += 0.3

            # context matches
            if cur_app and ep["context_app"] == cur_app:
                score += 0.2
            if cur_site and ep["context_site"] == cur_site:
                score += 0.1
            if cur_file and ep["context_file"] == cur_file:
                score += 0.1

            # only include successful episodes
            if ep["outcome"] == "failure":
                score *= 0.3

            if score > 0.2:
                ep["_score"] = round(score, 2)
                scored.append(ep)

        # sort by score descending
        scored.sort(key=lambda x: x["_score"], reverse=True)
        return scored[:limit]

    except Exception as e:
        print(f"Episodic similarity search error: {e}")
        return []


# -------------------------
# STATS
# -------------------------

def get_episode_stats():
    """
    Return summary stats — total episodes, success rate, top intents.
    """
    try:
        conn = _get_conn()

        total = conn.execute("SELECT COUNT(*) FROM episodes").fetchone()[0]
        success = conn.execute(
            "SELECT COUNT(*) FROM episodes WHERE outcome='success'"
        ).fetchone()[0]

        top_intents = conn.execute("""
            SELECT intent, COUNT(*) as cnt
            FROM episodes
            WHERE intent != ''
            GROUP BY intent
            ORDER BY cnt DESC LIMIT 5
        """).fetchall()

        conn.close()

        rate = round(success / total, 2) if total > 0 else 0.0

        return {
            "total": total,
            "success_rate": rate,
            "top_intents": [{"intent": r[0], "count": r[1]} for r in top_intents]
        }

    except Exception as e:
        print(f"Episode stats error: {e}")
        return {}


def print_stats():
    stats = get_episode_stats()
    print("\n--- Episode Stats ---")
    print(f"Total    : {stats.get('total', 0)}")
    print(f"Success  : {stats.get('success_rate', 0) * 100:.0f}%")
    print(f"Top acts : {stats.get('top_intents', [])}")
    print("---------------------\n")


# -------------------------
# HELPERS
# -------------------------

def _extract_intent(plan):
    if not plan:
        return ""
    if isinstance(plan, dict) and "workflow" in plan:
        steps = plan["workflow"]
        if steps:
            first = steps[0]
            return first.get("action") or first.get("intent") or ""
    if isinstance(plan, list) and plan:
        first = plan[0]
        if isinstance(first, dict):
            return first.get("intent") or ""
    return ""


def _row_to_dict(row):
    keys = ["command", "intent", "context_app", "context_win",
            "context_site", "context_file", "plan",
            "outcome", "verdict", "duration_ms", "timestamp"]
    d = dict(zip(keys, row))
    # parse plan back from JSON
    try:
        d["plan"] = json.loads(d["plan"]) if d["plan"] else None
    except:
        d["plan"] = None
    return d


def _words_overlap(a, b):
    """Count how many words two strings share."""
    set_a = set(a.split())
    set_b = set(b.split())
    return len(set_a & set_b)