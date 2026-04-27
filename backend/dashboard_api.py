# # backend/dashboard_api.py
# # STEP 123 — Web dashboard API
# # STEP 124 — Skill sharing
# # STEP 126 — Permissions endpoint

# import os
# import sys

# import sys as _sys
# import io


# import json
# from datetime import datetime
# from typing import Optional

# from fastapi import FastAPI, HTTPException, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse, JSONResponse
# from pydantic import BaseModel

# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# from memory.experience_memory import load_experiences
# from memory.episodic_memory import get_episode_stats
# from brain.pattern_recognizer import analyze_patterns
# from memory.knowledge_graph import top_nodes, get_related
# from skills.skills_registry import SKILLS
# from brain.context_memory import memory as ctx

# app = FastAPI(title="Fury Dashboard API", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://localhost:5173"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class CommandRequest(BaseModel):
#     command: str

# class PermissionRequest(BaseModel):
#     capability: str
#     status: str  # "always" | "deny" | "ask"

# # -------------------------
# # STATUS
# # -------------------------

# @app.get("/status")
# def get_status():
#     return {
#         "status": "running",
#         "timestamp": str(datetime.now()),
#         "context": {
#             "app":    ctx.get_app(),
#             "window": ctx.get_window(),
#             "site":   ctx.get_site(),
#             "file":   ctx.get_file(),
#             "action": ctx.get_action(),
#         }
#     }

# # -------------------------
# # HISTORY
# # -------------------------

# @app.get("/history")
# def get_history(limit: int = 20):
#     experiences = load_experiences()
#     recent = list(reversed(experiences))[:limit]
#     return {
#         "total": len(experiences),
#         "items": [
#             {
#                 "command":   exp.get("command"),
#                 "success":   exp.get("success"),
#                 "timestamp": exp.get("timestamp"),
#                 "plan_type": _plan_type(exp.get("plan")),
#                 "actions":   _plan_actions(exp.get("plan")),
#             }
#             for exp in recent
#         ]
#     }

# # -------------------------
# # EPISODES
# # -------------------------

# @app.get("/episodes")
# def get_episodes():
#     return get_episode_stats()

# # -------------------------
# # PATTERNS
# # -------------------------

# @app.get("/patterns")
# def get_patterns():
#     try:
#         return analyze_patterns()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




# # ADD THIS to dashboard_api.py
# # Place it after the existing /command endpoint (around line 100)
# # This is what makes the UI actually work — executes commands and returns output

# import io
# import sys as _sys

# @app.post("/chat")
# def chat_command(req: CommandRequest):
#     """
#     Execute a Fury command and return its output directly.
#     Unlike /command which just queues, this runs immediately.
#     """
#     command = req.command.strip()
#     if not command:
#         raise HTTPException(status_code=400, detail="Empty command")

#     # strip >>> prefix
#     while command.startswith(">"):
#         command = command.lstrip("> ").strip()

#     cmd = command.lower().strip()

#     # capture stdout
#     old_stdout = _sys.stdout
#     _sys.stdout = buf = io.StringIO()

#     output = ""
#     try:
#         # --- VISUAL ---
#         if cmd.startswith("visual "):
#             goal = command[7:].strip()
#             from execution.visual_agent import run_visual_goal
#             result = run_visual_goal(goal)
#             output = f"Outcome: {result['outcome']} in {result['steps']} steps"

#         # --- PROFILE ---
#         elif cmd in ("profile", "fury profile"):
#             from brain.personal_profile import profile
#             profile.show()

#         elif cmd == "fury profile reload":
#             from brain.personal_profile import profile
#             profile.reload()
#             output = "✅ Profile reloaded"

#         # --- TABS ---
#         elif cmd in ("tabs", "show tabs"):
#             from brain.tab_intelligence import print_open_tabs
#             print_open_tabs()

#         elif cmd.startswith("switch to "):
#             from brain.tab_intelligence import switch_to_tab
#             switch_to_tab(cmd.replace("switch to ", "").strip())
#             output = "✅ Switched"

#         # --- LEETCODE ---
#         elif cmd.startswith("leetcode "):
#             problem = command[9:].strip()
#             slug = problem.lower().replace(" ", "-")
#             url  = f"https://leetcode.com/problems/{slug}/"
#             from execution.visual_agent import run_visual_goal
#             result = run_visual_goal(
#                 f"open leetcode problem {problem}",
#                 context={"platform": "leetcode", "slug": slug, "url": url}
#             )
#             output = f"LeetCode: {result['outcome']} in {result['steps']} steps"

#         # --- JOB SEARCH ---
#         elif cmd.startswith("search jobs "):
#             rest  = command[12:].strip()
#             known = ["naukri","indeed","internshala","linkedin","unstop","wellfound"]
#             parts = rest.rsplit(" ", 1)
#             if len(parts) == 2 and parts[1].lower() in known:
#                 query, platform = parts[0], parts[1].lower()
#             else:
#                 query, platform = rest, "naukri"
#             from platforms.job_search_agent import search_jobs
#             search_jobs(query, platform)
#             output = f"✅ Opened {platform} search: {query}"

#         elif cmd.startswith("write cover letter "):
#             rest  = command[19:].strip().split(" ", 1)
#             role    = rest[0] if rest else "Developer"
#             company = rest[1] if len(rest) > 1 else "the company"
#             from platforms.job_search_agent import generate_cover_letter
#             generate_cover_letter(role, company)

#         elif cmd.startswith("draft email "):
#             rest  = command[12:].strip().split(" ", 2)
#             to      = rest[0] if rest else ""
#             role    = rest[1] if len(rest) > 1 else "Developer"
#             company = rest[2] if len(rest) > 2 else "the company"
#             from platforms.job_search_agent import draft_email
#             draft_email(to, role, company)

#         # --- WHATSAPP ---
#         elif cmd.startswith("whatsapp ") or cmd.startswith("send whatsapp "):
#             rest = command.replace("send whatsapp to ", "").replace("whatsapp ", "").strip()
#             if ":" in rest:
#                 contact, message = rest.split(":", 1)
#             else:
#                 parts = rest.split(" ", 1)
#                 contact = parts[0]
#                 message = parts[1] if len(parts) > 1 else ""
#             from execution.visual_agent import run_visual_goal
#             result = run_visual_goal(
#                 f"send whatsapp message to {contact.strip()}: {message.strip()}",
#                 context={"platform": "whatsapp", "contact": contact.strip()}
#             )
#             output = f"WhatsApp → {contact.strip()}: {result['outcome']}"

#         elif cmd in ("check whatsapp", "whatsapp unread"):
#             from execution.visual_agent import run_visual_goal
#             result = run_visual_goal("check whatsapp unread messages",
#                                      context={"platform": "whatsapp"})
#             output = f"WhatsApp check: {result['outcome']}"

#         # --- HISTORY ---
#         elif cmd in ("visual history", "fury visual history"):
#             from memory.task_memory import print_history
#             print_history()

#         elif cmd == "resume":
#             from execution.visual_agent import resume_last_task
#             resume_last_task()

#         # --- HELP ---
#         elif cmd == "fury help":
#             output = """FURY COMMANDS:
# visual <goal>          — visual play lofi on youtube
# leetcode <problem>     — leetcode two sum
# search jobs <role> <platform>
# write cover letter <role> <company>
# draft email <email> <role> <company>
# whatsapp <contact> <message>
# check whatsapp
# profile / fury profile reload
# tabs / switch to <platform>
# visual history / resume
# fury help"""

#         # --- MAIN PIPELINE ---
#         else:
#             from core.final_core import final_core
#             final_core.execute(command)

#     except Exception as e:
#         output = f"❌ Error: {e}"
#     finally:
#         _sys.stdout = old_stdout

#     captured = buf.getvalue().strip()
#     final_output = f"{captured}\n{output}".strip() if output else captured
#     return {"output": final_output or "✅ Done", "command": command}
# # -------------------------
# # REFLECTIONS
# # -------------------------

# @app.get("/reflections")
# def get_reflections(limit: int = 20):
#     _dir = os.path.dirname(os.path.abspath(__file__))
#     path = os.path.join(_dir, "memory", "reflections.json")
#     if not os.path.exists(path):
#         return {"items": []}
#     try:
#         with open(path, "r") as f:
#             data = json.load(f)
#         return {"items": list(reversed(data))[:limit]}
#     except:
#         return {"items": []}

# # -------------------------
# # KNOWLEDGE GRAPH
# # -------------------------

# @app.get("/knowledge")
# def get_knowledge(node_type: Optional[str] = None, limit: int = 20):
#     return {"nodes": top_nodes(node_type=node_type, limit=limit)}

# @app.get("/knowledge/{concept}")
# def get_concept(concept: str):
#     return get_related(concept)

# # -------------------------
# # SKILLS
# # -------------------------

# @app.get("/skills")
# def get_skills():
#     return {"skills": list(SKILLS.keys()), "count": len(SKILLS)}

# # -------------------------
# # SEND COMMAND
# # -------------------------

# @app.post("/command")
# def send_command(req: CommandRequest):
#     if not req.command or not req.command.strip():
#         raise HTTPException(status_code=400, detail="Empty command")
#     _dir = os.path.dirname(os.path.abspath(__file__))
#     queue_path = os.path.join(_dir, "memory", "command_queue.json")
#     try:
#         queue = []
#         if os.path.exists(queue_path):
#             with open(queue_path, "r") as f:
#                 queue = json.load(f)
#         queue.append({
#             "command": req.command.strip(),
#             "timestamp": str(datetime.now()),
#             "source": "dashboard"
#         })
#         with open(queue_path, "w") as f:
#             json.dump(queue, f, indent=2)
#         return {"status": "queued", "command": req.command}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # -------------------------
# # STEP 126 — PERMISSIONS
# # -------------------------

# @app.get("/permissions")
# def get_permissions():
#     try:
#         from core.permission_system import get_permissions_dict
#         return get_permissions_dict()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/permissions")
# def update_permission(req: PermissionRequest):
#     try:
#         from core.permission_system import (
#             grant_permission, deny_permission,
#             reset_permissions, CAPABILITIES, ASK
#         )
#         if req.capability not in CAPABILITIES:
#             raise HTTPException(status_code=400, detail=f"Unknown capability: {req.capability}")
#         if req.status == "always":
#             grant_permission(req.capability)
#         elif req.status == "deny":
#             deny_permission(req.capability)
#         elif req.status == "ask":
#             perms = {}
#             _dir = os.path.dirname(os.path.abspath(__file__))
#             path = os.path.join(_dir, "memory", "permissions.json")
#             if os.path.exists(path):
#                 with open(path, "r") as f:
#                     perms = json.load(f)
#             perms[req.capability] = ASK
#             with open(path, "w") as f:
#                 json.dump(perms, f, indent=2)
#         return {"status": "updated", "capability": req.capability, "value": req.status}
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # -------------------------
# # STEP 124 — SKILL SHARING
# # -------------------------

# @app.get("/skills/export")
# def export_skills():
#     import zipfile, tempfile
#     _dir = os.path.dirname(os.path.abspath(__file__))
#     skills_dir = os.path.join(_dir, "skills", "custom")
#     if not os.path.exists(skills_dir):
#         raise HTTPException(status_code=404, detail="No custom skills found")
#     skill_files = [f for f in os.listdir(skills_dir) if f.endswith(".py")]
#     if not skill_files:
#         raise HTTPException(status_code=404, detail="No custom skill files found")
#     tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
#     with zipfile.ZipFile(tmp.name, "w") as zf:
#         for fname in skill_files:
#             zf.write(os.path.join(skills_dir, fname), fname)
#     return FileResponse(tmp.name, media_type="application/zip", filename="fury_skills.zip")

# @app.post("/skills/import")
# async def import_skill(file: UploadFile = File(...)):
#     _dir = os.path.dirname(os.path.abspath(__file__))
#     skills_dir = os.path.join(_dir, "skills", "custom")
#     os.makedirs(skills_dir, exist_ok=True)
#     if not file.filename.endswith(".py"):
#         raise HTTPException(status_code=400, detail="Only .py skill files allowed")
#     content = await file.read()
#     dest = os.path.join(skills_dir, file.filename)
#     with open(dest, "wb") as f:
#         f.write(content)
#     return {"status": "imported", "filename": file.filename, "size": len(content)}

# @app.get("/skills/list-custom")
# def list_custom_skills():
#     _dir = os.path.dirname(os.path.abspath(__file__))
#     skills_dir = os.path.join(_dir, "skills", "custom")
#     if not os.path.exists(skills_dir):
#         return {"skills": []}
#     files = [f for f in os.listdir(skills_dir) if f.endswith(".py")]
#     result = []
#     for fname in files:
#         fpath = os.path.join(skills_dir, fname)
#         result.append({
#             "filename": fname,
#             "size": os.path.getsize(fpath),
#             "modified": datetime.fromtimestamp(os.path.getmtime(fpath)).isoformat()
#         })
#     return {"skills": result}

# # -------------------------
# # SAFETY INFO
# # -------------------------

# @app.get("/safety")
# def get_safety():
#     try:
#         from core.safety_sandbox import get_blocked_commands, sandbox_is_on
#         return {
#             "sandbox_mode": sandbox_is_on(),
#             "blocked_commands": get_blocked_commands()
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # -------------------------
# # HELPERS
# # -------------------------

# def _plan_type(plan):
#     if not plan: return "none"
#     if isinstance(plan, dict) and "workflow" in plan: return "workflow"
#     if isinstance(plan, list): return "list"
#     return "unknown"

# def _plan_actions(plan):
#     if not plan: return []
#     if isinstance(plan, dict) and "workflow" in plan:
#         actions = []
#         for s in plan.get("workflow", []):
#             if isinstance(s, dict):
#                 if s.get("action") == "skill":
#                     actions.append(f"skill:{s.get('data', {}).get('intent', '?')}")
#                 else:
#                     actions.append(s.get("action", "?"))
#         return actions
#     return []

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("dashboard_api:app", host="0.0.0.0", port=8000, reload=True)


    # REPLACE the entire /chat endpoint in dashboard_api.py with this version
# It handles natural language like "say hi to rishu on whatsapp"


# backend/dashboard_api.py
# STEP 123 — Web dashboard API
# STEP 124 — Skill sharing
# STEP 126 — Permissions endpoint
# STEP 141+ — /chat endpoint for React UI

import os
import sys
import io
import re
import json
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from memory.experience_memory import load_experiences
from memory.episodic_memory import get_episode_stats
from brain.pattern_recognizer import analyze_patterns
from memory.knowledge_graph import top_nodes, get_related
from skills.skills_registry import SKILLS
from brain.context_memory import memory as ctx

app = FastAPI(title="Fury Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CommandRequest(BaseModel):
    command: str


class PermissionRequest(BaseModel):
    capability: str
    status: str  # "always" | "deny" | "ask"


# ─────────────────────────────────────────
# STATUS
# ─────────────────────────────────────────

@app.get("/status")
def get_status():
    return {
        "status": "running",
        "timestamp": str(datetime.now()),
        "context": {
            "app":    ctx.get_app(),
            "window": ctx.get_window(),
            "site":   ctx.get_site(),
            "file":   ctx.get_file(),
            "action": ctx.get_action(),
        }
    }


# ─────────────────────────────────────────
# HISTORY
# ─────────────────────────────────────────

@app.get("/history")
def get_history(limit: int = 20):
    experiences = load_experiences()
    recent = list(reversed(experiences))[:limit]
    return {
        "total": len(experiences),
        "items": [
            {
                "command":   exp.get("command"),
                "success":   exp.get("success"),
                "timestamp": exp.get("timestamp"),
            }
            for exp in recent
        ]
    }


# ─────────────────────────────────────────
# EPISODES / PATTERNS / REFLECTIONS
# ─────────────────────────────────────────

@app.get("/episodes")
def get_episodes():
    return get_episode_stats()


@app.get("/patterns")
def get_patterns():
    try:
        return analyze_patterns()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reflections")
def get_reflections(limit: int = 20):
    _dir  = os.path.dirname(os.path.abspath(__file__))
    path  = os.path.join(_dir, "memory", "reflections.json")
    if not os.path.exists(path):
        return {"items": []}
    try:
        with open(path) as f:
            data = json.load(f)
        return {"items": list(reversed(data))[:limit]}
    except:
        return {"items": []}


# ─────────────────────────────────────────
# KNOWLEDGE
# ─────────────────────────────────────────

@app.get("/knowledge")
def get_knowledge(node_type: Optional[str] = None, limit: int = 20):
    return {"nodes": top_nodes(node_type=node_type, limit=limit)}


@app.get("/knowledge/{concept}")
def get_concept(concept: str):
    return get_related(concept)


# ─────────────────────────────────────────
# SKILLS
# ─────────────────────────────────────────

@app.get("/skills")
def get_skills():
    return {"skills": list(SKILLS.keys()), "count": len(SKILLS)}


# ─────────────────────────────────────────
# COMMAND QUEUE (old — keeps compatibility)
# ─────────────────────────────────────────

@app.post("/command")
def send_command(req: CommandRequest):
    if not req.command or not req.command.strip():
        raise HTTPException(status_code=400, detail="Empty command")
    _dir = os.path.dirname(os.path.abspath(__file__))
    queue_path = os.path.join(_dir, "memory", "command_queue.json")
    try:
        queue = []
        if os.path.exists(queue_path):
            with open(queue_path) as f:
                queue = json.load(f)
        queue.append({
            "command":   req.command.strip(),
            "timestamp": str(datetime.now()),
            "source":    "dashboard"
        })
        with open(queue_path, "w") as f:
            json.dump(queue, f, indent=2)
        return {"status": "queued", "command": req.command}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# PERMISSIONS
# ─────────────────────────────────────────

@app.get("/permissions")
def get_permissions():
    try:
        from core.permission_system import get_permissions_dict
        return get_permissions_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/permissions")
def update_permission(req: PermissionRequest):
    try:
        from core.permission_system import (
            grant_permission, deny_permission, CAPABILITIES, ASK
        )
        if req.capability not in CAPABILITIES:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown capability: {req.capability}"
            )
        if req.status == "always":
            grant_permission(req.capability)
        elif req.status == "deny":
            deny_permission(req.capability)
        elif req.status == "ask":
            _dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(_dir, "memory", "permissions.json")
            perms = {}
            if os.path.exists(path):
                with open(path) as f:
                    perms = json.load(f)
            perms[req.capability] = ASK
            with open(path, "w") as f:
                json.dump(perms, f, indent=2)
        return {"status": "updated",
                "capability": req.capability, "value": req.status}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# SKILL SHARING
# ─────────────────────────────────────────

@app.get("/skills/export")
def export_skills():
    import zipfile, tempfile
    _dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(_dir, "skills", "custom")
    if not os.path.exists(skills_dir):
        raise HTTPException(status_code=404, detail="No custom skills found")
    skill_files = [f for f in os.listdir(skills_dir) if f.endswith(".py")]
    if not skill_files:
        raise HTTPException(status_code=404, detail="No custom skill files")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    with zipfile.ZipFile(tmp.name, "w") as zf:
        for fname in skill_files:
            zf.write(os.path.join(skills_dir, fname), fname)
    return FileResponse(tmp.name,
                        media_type="application/zip",
                        filename="fury_skills.zip")


@app.post("/skills/import")
async def import_skill(file: UploadFile = File(...)):
    _dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(_dir, "skills", "custom")
    os.makedirs(skills_dir, exist_ok=True)
    if not file.filename.endswith(".py"):
        raise HTTPException(status_code=400,
                            detail="Only .py skill files allowed")
    content = await file.read()
    with open(os.path.join(skills_dir, file.filename), "wb") as f:
        f.write(content)
    return {"status": "imported",
            "filename": file.filename, "size": len(content)}


@app.get("/skills/list-custom")
def list_custom_skills():
    _dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(_dir, "skills", "custom")
    if not os.path.exists(skills_dir):
        return {"skills": []}
    files = [f for f in os.listdir(skills_dir) if f.endswith(".py")]
    return {
        "skills": [
            {
                "filename": f,
                "size":     os.path.getsize(os.path.join(skills_dir, f)),
                "modified": datetime.fromtimestamp(
                    os.path.getmtime(os.path.join(skills_dir, f))
                ).isoformat()
            }
            for f in files
        ]
    }


# ─────────────────────────────────────────
# SAFETY
# ─────────────────────────────────────────

@app.get("/safety")
def get_safety():
    try:
        from core.safety_sandbox import get_blocked_commands, sandbox_is_on
        return {
            "sandbox_mode":     sandbox_is_on(),
            "blocked_commands": get_blocked_commands()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# /chat — MAIN UI ENDPOINT
# Executes commands and returns output to React UI
# Uses commands/ folder for routing (same as fury.py)
# ─────────────────────────────────────────

@app.post("/chat")
def chat_command(req: CommandRequest):
    """Execute a Fury command and return output to the UI."""
    command = req.command.strip()
    if not command:
        raise HTTPException(status_code=400, detail="Empty command")

    # strip >>> prefix
    while command.startswith(">"):
        command = command.lstrip("> ").strip()
    if not command:
        return {"output": "Empty command", "command": command}

    cmd = command.lower().strip()

    # capture stdout so terminal output goes back to UI
    old_stdout = sys.stdout
    sys.stdout  = buf = io.StringIO()
    output      = ""

    try:
        # ── route through same command files as fury.py ──
        from commands.visual_commands   import handle as visual_handle
        from commands.platform_commands import handle as platform_handle
        from commands.job_commands      import handle as job_handle
        from commands.code_commands     import handle as code_handle
        from commands.system_commands   import handle as system_handle

        handled = (
            visual_handle(command, cmd)   or
            platform_handle(command, cmd) or
            job_handle(command, cmd)      or
            code_handle(command, cmd)     or
            system_handle(command, cmd)
        )

        # ── natural language fallback ──
        if not handled:
            nl_type, nl_data = _parse_natural(command)

            if nl_type == "whatsapp_send":
                from execution.visual_agent import run_visual_goal
                contact = nl_data["contact"]
                message = nl_data["message"]
                result  = run_visual_goal(
                    f"send whatsapp message to {contact}: {message}",
                    context={"platform": "whatsapp", "contact": contact}
                )
                output = f"💬 WhatsApp → {contact}: {result['outcome']}"

            elif nl_type == "whatsapp_check":
                from execution.visual_agent import run_visual_goal
                result = run_visual_goal("check whatsapp unread messages",
                                         context={"platform": "whatsapp"})
                output = f"💬 WhatsApp: {result['outcome']}"

            elif nl_type == "youtube":
                from execution.visual_agent import run_visual_goal
                result = run_visual_goal(
                    f"play {nl_data['query']} on youtube",
                    context={"platform": "youtube"}
                )
                output = f"🎵 YouTube: {result['outcome']}"

            elif nl_type == "leetcode":
                problem = nl_data["problem"]
                slug    = problem.lower().replace(" ", "-")
                from execution.visual_agent import run_visual_goal
                result  = run_visual_goal(
                    f"open leetcode problem {problem}",
                    context={"platform": "leetcode",
                             "slug": slug,
                             "url": f"https://leetcode.com/problems/{slug}/"}
                )
                output = f"🧩 LeetCode: {result['outcome']}"

            elif nl_type == "job_search":
                from platforms.job_search_agent import search_jobs
                search_jobs(nl_data["query"],
                            nl_data.get("platform", "naukri"))
                output = f"🔍 Searching: {nl_data['query']}"

            elif nl_type == "telegram_send":
                from execution.visual_agent import run_visual_goal
                contact = nl_data["contact"]
                message = nl_data["message"]
                result  = run_visual_goal(
                    f"send telegram to {contact}: {message}",
                    context={"platform": "telegram", "contact": contact}
                )
                output = f"✈️ Telegram → {contact}: {result['outcome']}"

            else:
                output = (
                    f"❓ Not recognised: '{command}'\n\n"
                    f"Try: play <song> on youtube\n"
                    f"     say hi to <contact> on whatsapp\n"
                    f"     leetcode <problem>\n"
                    f"     fury help"
                )

    except Exception as e:
        output = f"❌ Error: {e}"
    finally:
        sys.stdout = old_stdout

    captured = buf.getvalue().strip()
    final    = f"{captured}\n{output}".strip() if output else captured
    return {"output": final or "✅ Done", "command": command}


# ─────────────────────────────────────────
# NATURAL LANGUAGE PARSER
# ─────────────────────────────────────────

def _parse_natural(command):
    cmd = command.lower().strip()

    # WhatsApp send
    wa_patterns = [
        r"(?:say|send|message|tell|write)\s+(.+?)\s+to\s+(\w+)\s+on\s+whatsapp",
        r"whatsapp\s+(\w+)\s+(.+)",
    ]
    for pat in wa_patterns:
        m = re.search(pat, cmd)
        if m:
            g = m.groups()
            if "to" in cmd and "whatsapp" in cmd:
                message, contact = g[0].strip(), g[1].strip().title()
            else:
                contact, message = g[0].strip().title(), g[1].strip()
            return "whatsapp_send", {"contact": contact, "message": message}

    if any(p in cmd for p in ["check whatsapp", "whatsapp unread"]):
        return "whatsapp_check", {}

    # YouTube
    for pat in [
        r"(?:play|listen to|watch)\s+(.+?)\s+on\s+youtube",
        r"(?:play|listen to)\s+(.+)",
    ]:
        m = re.search(pat, cmd)
        if m and ("youtube" in cmd or "play" in cmd):
            q = m.group(1).strip()
            if q:
                return "youtube", {"query": q}

    # LeetCode
    m = re.search(r"(?:solve|open|do)\s+(.+?)\s+(?:on\s+)?leetcode", cmd)
    if m:
        return "leetcode", {"problem": m.group(1).strip()}

    # Job search
    m = re.search(r"(?:find|search)\s+(.+?)\s+jobs?\s+on\s+(\w+)", cmd)
    if m:
        return "job_search", {"query": m.group(1), "platform": m.group(2)}

    # Telegram
    for pat in [
        r"(?:say|send|message)\s+(.+?)\s+to\s+(\w+)\s+on\s+telegram",
        r"telegram\s+(\w+)\s+(.+)",
    ]:
        m = re.search(pat, cmd)
        if m:
            g = m.groups()
            if "to" in cmd:
                message, contact = g[0].strip(), g[1].strip().title()
            else:
                contact, message = g[0].strip().title(), g[1].strip()
            return "telegram_send", {"contact": contact, "message": message}

    return None, None


# ─────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("dashboard_api:app",
                host="0.0.0.0", port=8000, reload=True)