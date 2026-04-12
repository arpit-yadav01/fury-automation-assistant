# backend/dashboard_api.py
# STEP 123 — Web dashboard API
# STEP 124 — Skill sharing
# STEP 126 — Permissions endpoint

import os
import sys
import json
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

# -------------------------
# STATUS
# -------------------------

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

# -------------------------
# HISTORY
# -------------------------

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
                "plan_type": _plan_type(exp.get("plan")),
                "actions":   _plan_actions(exp.get("plan")),
            }
            for exp in recent
        ]
    }

# -------------------------
# EPISODES
# -------------------------

@app.get("/episodes")
def get_episodes():
    return get_episode_stats()

# -------------------------
# PATTERNS
# -------------------------

@app.get("/patterns")
def get_patterns():
    try:
        return analyze_patterns()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# REFLECTIONS
# -------------------------

@app.get("/reflections")
def get_reflections(limit: int = 20):
    _dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(_dir, "memory", "reflections.json")
    if not os.path.exists(path):
        return {"items": []}
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return {"items": list(reversed(data))[:limit]}
    except:
        return {"items": []}

# -------------------------
# KNOWLEDGE GRAPH
# -------------------------

@app.get("/knowledge")
def get_knowledge(node_type: Optional[str] = None, limit: int = 20):
    return {"nodes": top_nodes(node_type=node_type, limit=limit)}

@app.get("/knowledge/{concept}")
def get_concept(concept: str):
    return get_related(concept)

# -------------------------
# SKILLS
# -------------------------

@app.get("/skills")
def get_skills():
    return {"skills": list(SKILLS.keys()), "count": len(SKILLS)}

# -------------------------
# SEND COMMAND
# -------------------------

@app.post("/command")
def send_command(req: CommandRequest):
    if not req.command or not req.command.strip():
        raise HTTPException(status_code=400, detail="Empty command")
    _dir = os.path.dirname(os.path.abspath(__file__))
    queue_path = os.path.join(_dir, "memory", "command_queue.json")
    try:
        queue = []
        if os.path.exists(queue_path):
            with open(queue_path, "r") as f:
                queue = json.load(f)
        queue.append({
            "command": req.command.strip(),
            "timestamp": str(datetime.now()),
            "source": "dashboard"
        })
        with open(queue_path, "w") as f:
            json.dump(queue, f, indent=2)
        return {"status": "queued", "command": req.command}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# STEP 126 — PERMISSIONS
# -------------------------

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
            grant_permission, deny_permission,
            reset_permissions, CAPABILITIES, ASK
        )
        if req.capability not in CAPABILITIES:
            raise HTTPException(status_code=400, detail=f"Unknown capability: {req.capability}")
        if req.status == "always":
            grant_permission(req.capability)
        elif req.status == "deny":
            deny_permission(req.capability)
        elif req.status == "ask":
            perms = {}
            _dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(_dir, "memory", "permissions.json")
            if os.path.exists(path):
                with open(path, "r") as f:
                    perms = json.load(f)
            perms[req.capability] = ASK
            with open(path, "w") as f:
                json.dump(perms, f, indent=2)
        return {"status": "updated", "capability": req.capability, "value": req.status}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# STEP 124 — SKILL SHARING
# -------------------------

@app.get("/skills/export")
def export_skills():
    import zipfile, tempfile
    _dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(_dir, "skills", "custom")
    if not os.path.exists(skills_dir):
        raise HTTPException(status_code=404, detail="No custom skills found")
    skill_files = [f for f in os.listdir(skills_dir) if f.endswith(".py")]
    if not skill_files:
        raise HTTPException(status_code=404, detail="No custom skill files found")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    with zipfile.ZipFile(tmp.name, "w") as zf:
        for fname in skill_files:
            zf.write(os.path.join(skills_dir, fname), fname)
    return FileResponse(tmp.name, media_type="application/zip", filename="fury_skills.zip")

@app.post("/skills/import")
async def import_skill(file: UploadFile = File(...)):
    _dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(_dir, "skills", "custom")
    os.makedirs(skills_dir, exist_ok=True)
    if not file.filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="Only .py skill files allowed")
    content = await file.read()
    dest = os.path.join(skills_dir, file.filename)
    with open(dest, "wb") as f:
        f.write(content)
    return {"status": "imported", "filename": file.filename, "size": len(content)}

@app.get("/skills/list-custom")
def list_custom_skills():
    _dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(_dir, "skills", "custom")
    if not os.path.exists(skills_dir):
        return {"skills": []}
    files = [f for f in os.listdir(skills_dir) if f.endswith(".py")]
    result = []
    for fname in files:
        fpath = os.path.join(skills_dir, fname)
        result.append({
            "filename": fname,
            "size": os.path.getsize(fpath),
            "modified": datetime.fromtimestamp(os.path.getmtime(fpath)).isoformat()
        })
    return {"skills": result}

# -------------------------
# SAFETY INFO
# -------------------------

@app.get("/safety")
def get_safety():
    try:
        from core.safety_sandbox import get_blocked_commands, sandbox_is_on
        return {
            "sandbox_mode": sandbox_is_on(),
            "blocked_commands": get_blocked_commands()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# HELPERS
# -------------------------

def _plan_type(plan):
    if not plan: return "none"
    if isinstance(plan, dict) and "workflow" in plan: return "workflow"
    if isinstance(plan, list): return "list"
    return "unknown"

def _plan_actions(plan):
    if not plan: return []
    if isinstance(plan, dict) and "workflow" in plan:
        actions = []
        for s in plan.get("workflow", []):
            if isinstance(s, dict):
                if s.get("action") == "skill":
                    actions.append(f"skill:{s.get('data', {}).get('intent', '?')}")
                else:
                    actions.append(s.get("action", "?"))
        return actions
    return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("dashboard_api:app", host="0.0.0.0", port=8000, reload=True)