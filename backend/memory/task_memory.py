# memory/task_memory.py
# STEP 132 — Task Memory
#
# Saves the full state of a running visual agent task to disk.
# If Fury is interrupted (crash, exit, error), it can resume
# from exactly where it left off instead of starting over.
#
# Also tracks task history — every goal attempted, outcome, steps taken.
#
# Used by visual_agent.py — save state after each step,
# restore state on resume.

import os
import json
from datetime import datetime

_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_FILE    = os.path.join(_DIR, "current_task.json")
HISTORY_FILE = os.path.join(_DIR, "task_history.json")


# -------------------------
# SAVE CURRENT TASK STATE
# Called after every step in visual_agent.py
# -------------------------

def save_task_state(goal, steps_taken, step_num, outcome="running", context=None):
    """
    Save the current state of a running task.

    Args:
        goal: the goal string
        steps_taken: list of steps completed so far
        step_num: current step number
        outcome: "running" | "success" | "failed" | "stuck" | "max_steps"
        context: optional extra context dict
    """
    state = {
        "goal": goal,
        "step_num": step_num,
        "steps_taken": steps_taken,
        "outcome": outcome,
        "context": context or {},
        "saved_at": str(datetime.now()),
    }
    try:
        os.makedirs(_DIR, exist_ok=True)
        with open(TASK_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Task memory save error: {e}")


# -------------------------
# LOAD CURRENT TASK STATE
# Called on startup or resume command
# -------------------------

def load_task_state():
    """
    Load the last saved task state.
    Returns the state dict or None if no saved task.
    """
    if not os.path.exists(TASK_FILE):
        return None
    try:
        with open(TASK_FILE, "r") as f:
            state = json.load(f)
        # only return if task was still running
        if state.get("outcome") == "running":
            return state
        return None
    except Exception as e:
        print(f"Task memory load error: {e}")
        return None


def clear_task_state():
    """Clear the current task state (call when task completes)."""
    if os.path.exists(TASK_FILE):
        try:
            # mark as completed rather than delete
            with open(TASK_FILE, "r") as f:
                state = json.load(f)
            state["outcome"] = "completed"
            with open(TASK_FILE, "w") as f:
                json.dump(state, f, indent=2)
        except:
            pass


def has_pending_task():
    """Returns True if there's an interrupted task that can be resumed."""
    state = load_task_state()
    return state is not None


def get_pending_task_summary():
    """Returns a human-readable summary of the pending task."""
    state = load_task_state()
    if not state:
        return None
    return {
        "goal": state.get("goal"),
        "steps_completed": state.get("step_num", 0),
        "saved_at": state.get("saved_at"),
    }


# -------------------------
# TASK HISTORY
# Logs every completed task
# -------------------------

def save_to_history(goal, outcome, steps, duration_ms, context=None):
    """
    Append a completed task to history log.
    Called when visual_agent finishes (any outcome).
    """
    entry = {
        "goal": goal,
        "outcome": outcome,
        "steps": steps,
        "duration_ms": duration_ms,
        "context": context or {},
        "timestamp": str(datetime.now()),
    }
    try:
        os.makedirs(_DIR, exist_ok=True)
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        history.append(entry)
        # keep last 100 tasks
        history = history[-100:]
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Task history save error: {e}")


def load_history(limit=20):
    """Load recent task history."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
        return list(reversed(history))[:limit]
    except:
        return []


def get_history_stats():
    """Return stats about task history."""
    history = load_history(limit=100)
    if not history:
        return {"total": 0, "success_rate": 0, "avg_steps": 0}

    total = len(history)
    success = sum(1 for h in history if h.get("outcome") == "success")
    avg_steps = sum(h.get("steps", 0) for h in history) / total

    return {
        "total": total,
        "success_rate": round(success / total, 2),
        "avg_steps": round(avg_steps, 1),
        "recent": history[:5]
    }


def print_history():
    """Print recent task history."""
    history = load_history(limit=10)
    stats = get_history_stats()

    print("\n--- Visual Task History ---")
    print(f"Total: {stats['total']} | Success: {stats['success_rate']*100:.0f}% | Avg steps: {stats['avg_steps']}")
    print()
    for h in history:
        icon = "✅" if h["outcome"] == "success" else "❌"
        print(f"  {icon} [{h['outcome']:<10}] {h['goal'][:50]}")
        print(f"      Steps: {h['steps']} | Time: {h['duration_ms']}ms | {h['timestamp'][:19]}")
    print("---------------------------\n")