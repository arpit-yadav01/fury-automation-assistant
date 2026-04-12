# # memory/knowledge_graph.py
# # STEP 118 — Knowledge graph
# #
# # Builds a graph of connected concepts from Fury's experiences.
# # Nodes = entities (apps, files, commands, intents, sites)
# # Edges = relationships (used_with, leads_to, is_type, failed_with)
# #
# # Uses knowledge.db (existing) — adds two new tables: nodes + edges
# # Plugs into final_core.py → after_step()
# #
# # Over time the graph answers questions like:
# #   "what apps does the user use with python files?"
# #   "what commands usually follow opening youtube?"
# #   "what intent leads to most failures?"

# import sqlite3
# import os
# import json
# from datetime import datetime

# DB = os.path.join("memory", "knowledge.db")

# # -------------------------
# # DB SETUP
# # -------------------------

# def _get_conn():
#     os.makedirs("memory", exist_ok=True)
#     conn = sqlite3.connect(DB)
#     _create_tables(conn)
#     return conn


# def _create_tables(conn):
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS kg_nodes (
#             id        INTEGER PRIMARY KEY AUTOINCREMENT,
#             name      TEXT UNIQUE,
#             node_type TEXT,
#             count     INTEGER DEFAULT 1,
#             updated   TEXT
#         )
#     """)
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS kg_edges (
#             id           INTEGER PRIMARY KEY AUTOINCREMENT,
#             source       TEXT,
#             relation     TEXT,
#             target       TEXT,
#             weight       REAL DEFAULT 1.0,
#             updated      TEXT,
#             UNIQUE(source, relation, target)
#         )
#     """)
#     conn.commit()


# # -------------------------
# # NODE OPERATIONS
# # -------------------------

# def add_node(name, node_type="concept"):
#     """Add or increment a node."""
#     if not name or not name.strip():
#         return
#     name = name.lower().strip()
#     try:
#         conn = _get_conn()
#         existing = conn.execute(
#             "SELECT id, count FROM kg_nodes WHERE name=?", (name,)
#         ).fetchone()
#         if existing:
#             conn.execute(
#                 "UPDATE kg_nodes SET count=?, updated=? WHERE name=?",
#                 (existing[1] + 1, str(datetime.now()), name)
#             )
#         else:
#             conn.execute(
#                 "INSERT INTO kg_nodes (name, node_type, count, updated) VALUES (?,?,1,?)",
#                 (name, node_type, str(datetime.now()))
#             )
#         conn.commit()
#         conn.close()
#     except Exception as e:
#         print(f"KG add_node error: {e}")


# def get_node(name):
#     """Get a node by name."""
#     try:
#         conn = _get_conn()
#         row = conn.execute(
#             "SELECT name, node_type, count FROM kg_nodes WHERE name=?",
#             (name.lower().strip(),)
#         ).fetchone()
#         conn.close()
#         if row:
#             return {"name": row[0], "type": row[1], "count": row[2]}
#         return None
#     except:
#         return None


# # -------------------------
# # EDGE OPERATIONS
# # -------------------------

# def add_edge(source, relation, target, weight=1.0):
#     """
#     Add or strengthen an edge between two nodes.
#     Automatically creates nodes if they don't exist.
#     """
#     if not source or not target or not relation:
#         return
#     source  = source.lower().strip()
#     target  = target.lower().strip()
#     relation = relation.lower().strip()

#     add_node(source)
#     add_node(target)

#     try:
#         conn = _get_conn()
#         existing = conn.execute(
#             "SELECT id, weight FROM kg_edges WHERE source=? AND relation=? AND target=?",
#             (source, relation, target)
#         ).fetchone()
#         if existing:
#             new_weight = round(existing[1] + weight, 2)
#             conn.execute(
#                 "UPDATE kg_edges SET weight=?, updated=? WHERE id=?",
#                 (new_weight, str(datetime.now()), existing[0])
#             )
#         else:
#             conn.execute(
#                 "INSERT INTO kg_edges (source, relation, target, weight, updated) VALUES (?,?,?,?,?)",
#                 (source, relation, target, weight, str(datetime.now()))
#             )
#         conn.commit()
#         conn.close()
#     except Exception as e:
#         print(f"KG add_edge error: {e}")


# def get_edges(source, relation=None, limit=10):
#     """Get all edges from a source node, optionally filtered by relation."""
#     try:
#         conn = _get_conn()
#         if relation:
#             rows = conn.execute(
#                 "SELECT source, relation, target, weight FROM kg_edges "
#                 "WHERE source=? AND relation=? ORDER BY weight DESC LIMIT ?",
#                 (source.lower().strip(), relation, limit)
#             ).fetchall()
#         else:
#             rows = conn.execute(
#                 "SELECT source, relation, target, weight FROM kg_edges "
#                 "WHERE source=? ORDER BY weight DESC LIMIT ?",
#                 (source.lower().strip(), limit)
#             ).fetchall()
#         conn.close()
#         return [
#             {"source": r[0], "relation": r[1], "target": r[2], "weight": r[3]}
#             for r in rows
#         ]
#     except Exception as e:
#         print(f"KG get_edges error: {e}")
#         return []


# def get_related(concept, limit=5):
#     """
#     Get everything related to a concept — both outgoing and incoming edges.
#     Useful for: "what does Fury know about notepad?"
#     """
#     concept = concept.lower().strip()
#     try:
#         conn = _get_conn()
#         outgoing = conn.execute(
#             "SELECT relation, target, weight FROM kg_edges "
#             "WHERE source=? ORDER BY weight DESC LIMIT ?",
#             (concept, limit)
#         ).fetchall()
#         incoming = conn.execute(
#             "SELECT source, relation, weight FROM kg_edges "
#             "WHERE target=? ORDER BY weight DESC LIMIT ?",
#             (concept, limit)
#         ).fetchall()
#         conn.close()
#         return {
#             "concept": concept,
#             "knows": [{"relation": r[0], "target": r[1], "weight": r[2]} for r in outgoing],
#             "known_by": [{"source": r[0], "relation": r[1], "weight": r[2]} for r in incoming]
#         }
#     except Exception as e:
#         print(f"KG get_related error: {e}")
#         return {}


# # -------------------------
# # LEARN FROM EXECUTION
# # -------------------------

# def learn_from_execution(command, plan, outcome="success"):
#     """
#     Main entry point — call after every execution.
#     Extracts entities from command+plan and builds graph edges.

#     Called from final_core.py → after_step()
#     """
#     if not command:
#         return

#     cmd = command.lower().strip()

#     # extract intent
#     intent = _extract_intent(plan)

#     # node: command itself
#     add_node(cmd, node_type="command")

#     if intent:
#         add_node(intent, node_type="intent")
#         # command → used_intent → intent
#         add_edge(cmd, "used_intent", intent)

#     # edges from context
#     _learn_from_plan(cmd, intent, plan, outcome)


# def _learn_from_plan(cmd, intent, plan, outcome):
#     """Extract entities from plan and build edges."""

#     if not plan:
#         return

#     steps = []
#     if isinstance(plan, dict) and "workflow" in plan:
#         steps = plan["workflow"]
#     elif isinstance(plan, list):
#         steps = plan

#     for step in steps:
#         if not isinstance(step, dict):
#             continue

#         action = step.get("action") or step.get("intent") or ""

#         # app edges
#         app = step.get("name") or step.get("app") or ""
#         if app:
#             add_node(app, node_type="app")
#             add_edge(cmd, "opens", app)
#             if intent:
#                 add_edge(intent, "uses_app", app)

#         # url/site edges
#         url = step.get("url") or ""
#         if url:
#             site = _extract_site(url)
#             if site:
#                 add_node(site, node_type="site")
#                 add_edge(cmd, "visits", site)

#         # file edges
#         path = step.get("path") or step.get("filename") or ""
#         if path:
#             ext = path.rsplit(".", 1)[-1] if "." in path else ""
#             add_node(path, node_type="file")
#             add_edge(cmd, "creates_file", path)
#             if ext:
#                 add_node(ext, node_type="file_type")
#                 add_edge(path, "has_type", ext)

#         # outcome edges
#         if outcome == "failure" and action:
#             add_edge(cmd, "failed_at", action, weight=0.5)
#         elif outcome == "success" and action:
#             add_edge(cmd, "succeeded_with", action, weight=1.0)


# def _extract_intent(plan):
#     if not plan:
#         return ""
#     if isinstance(plan, dict) and "workflow" in plan:
#         steps = plan.get("workflow", [])
#         if steps and isinstance(steps[0], dict):
#             return steps[0].get("action") or steps[0].get("intent") or ""
#     if isinstance(plan, list) and plan:
#         if isinstance(plan[0], dict):
#             return plan[0].get("intent") or ""
#     return ""


# def _extract_site(url):
#     """Extract site name from URL."""
#     for site in ["youtube", "google", "github", "stackoverflow", "twitter"]:
#         if site in url:
#             return site
#     return ""


# # -------------------------
# # QUERY HELPERS
# # -------------------------

# def what_does_fury_know_about(concept):
#     """Human-readable summary of what's in the graph for a concept."""
#     related = get_related(concept)
#     if not related:
#         print(f"Fury knows nothing about '{concept}' yet.")
#         return

#     print(f"\n--- Fury knows about '{concept}' ---")
#     for item in related.get("knows", []):
#         print(f"  {concept} --[{item['relation']}]--> {item['target']}  (w={item['weight']})")
#     for item in related.get("known_by", []):
#         print(f"  {item['source']} --[{item['relation']}]--> {concept}  (w={item['weight']})")
#     print("---\n")


# def top_nodes(node_type=None, limit=5):
#     """Return most frequently seen nodes."""
#     try:
#         conn = _get_conn()
#         if node_type:
#             rows = conn.execute(
#                 "SELECT name, count FROM kg_nodes WHERE node_type=? "
#                 "ORDER BY count DESC LIMIT ?",
#                 (node_type, limit)
#             ).fetchall()
#         else:
#             rows = conn.execute(
#                 "SELECT name, count FROM kg_nodes ORDER BY count DESC LIMIT ?",
#                 (limit,)
#             ).fetchall()
#         conn.close()
#         return [{"name": r[0], "count": r[1]} for r in rows]
#     except:
#         return []



# memory/knowledge_graph.py
# STEP 118 — Knowledge graph
# FIX: absolute path so DB works regardless of working directory

import sqlite3
import os
import json
from datetime import datetime

# ✅ FIX: path relative to this file, not cwd
_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(_DIR, "knowledge.db")


def _get_conn():
    os.makedirs(_DIR, exist_ok=True)
    conn = sqlite3.connect(DB)
    _create_tables(conn)
    return conn


def _create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS kg_nodes (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT UNIQUE,
            node_type TEXT,
            count     INTEGER DEFAULT 1,
            updated   TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS kg_edges (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            source       TEXT,
            relation     TEXT,
            target       TEXT,
            weight       REAL DEFAULT 1.0,
            updated      TEXT,
            UNIQUE(source, relation, target)
        )
    """)
    conn.commit()


def add_node(name, node_type="concept"):
    if not name or not str(name).strip():
        return
    name = str(name).lower().strip()
    try:
        conn = _get_conn()
        existing = conn.execute(
            "SELECT id, count FROM kg_nodes WHERE name=?", (name,)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE kg_nodes SET count=?, updated=? WHERE name=?",
                (existing[1] + 1, str(datetime.now()), name)
            )
        else:
            conn.execute(
                "INSERT INTO kg_nodes (name, node_type, count, updated) VALUES (?,?,1,?)",
                (name, node_type, str(datetime.now()))
            )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"KG add_node error: {e}")


def get_node(name):
    try:
        conn = _get_conn()
        row = conn.execute(
            "SELECT name, node_type, count FROM kg_nodes WHERE name=?",
            (name.lower().strip(),)
        ).fetchone()
        conn.close()
        return {"name": row[0], "type": row[1], "count": row[2]} if row else None
    except:
        return None


def add_edge(source, relation, target, weight=1.0):
    if not source or not target or not relation:
        return
    source   = str(source).lower().strip()
    target   = str(target).lower().strip()
    relation = str(relation).lower().strip()
    add_node(source)
    add_node(target)
    try:
        conn = _get_conn()
        existing = conn.execute(
            "SELECT id, weight FROM kg_edges WHERE source=? AND relation=? AND target=?",
            (source, relation, target)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE kg_edges SET weight=?, updated=? WHERE id=?",
                (round(existing[1] + weight, 2), str(datetime.now()), existing[0])
            )
        else:
            conn.execute(
                "INSERT INTO kg_edges (source, relation, target, weight, updated) VALUES (?,?,?,?,?)",
                (source, relation, target, weight, str(datetime.now()))
            )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"KG add_edge error: {e}")


def get_edges(source, relation=None, limit=10):
    try:
        conn = _get_conn()
        if relation:
            rows = conn.execute(
                "SELECT source, relation, target, weight FROM kg_edges "
                "WHERE source=? AND relation=? ORDER BY weight DESC LIMIT ?",
                (source.lower().strip(), relation, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT source, relation, target, weight FROM kg_edges "
                "WHERE source=? ORDER BY weight DESC LIMIT ?",
                (source.lower().strip(), limit)
            ).fetchall()
        conn.close()
        return [{"source": r[0], "relation": r[1], "target": r[2], "weight": r[3]} for r in rows]
    except Exception as e:
        print(f"KG get_edges error: {e}")
        return []


def get_related(concept, limit=5):
    concept = concept.lower().strip()
    try:
        conn = _get_conn()
        outgoing = conn.execute(
            "SELECT relation, target, weight FROM kg_edges "
            "WHERE source=? ORDER BY weight DESC LIMIT ?",
            (concept, limit)
        ).fetchall()
        incoming = conn.execute(
            "SELECT source, relation, weight FROM kg_edges "
            "WHERE target=? ORDER BY weight DESC LIMIT ?",
            (concept, limit)
        ).fetchall()
        conn.close()
        return {
            "concept": concept,
            "knows":    [{"relation": r[0], "target": r[1], "weight": r[2]} for r in outgoing],
            "known_by": [{"source": r[0], "relation": r[1], "weight": r[2]} for r in incoming]
        }
    except Exception as e:
        print(f"KG get_related error: {e}")
        return {}


def learn_from_execution(command, plan, outcome="success"):
    if not command:
        return
    cmd = command.lower().strip()
    intent = _extract_intent(plan)
    add_node(cmd, node_type="command")
    if intent:
        add_node(intent, node_type="intent")
        add_edge(cmd, "used_intent", intent)
    _learn_from_plan(cmd, intent, plan, outcome)


def _learn_from_plan(cmd, intent, plan, outcome):
    if not plan:
        return
    steps = []
    if isinstance(plan, dict) and "workflow" in plan:
        steps = plan["workflow"]
    elif isinstance(plan, list):
        steps = plan

    for step in steps:
        if not isinstance(step, dict):
            continue
        action = step.get("action") or step.get("intent") or ""
        app = step.get("name") or step.get("app") or ""
        if app:
            add_node(app, node_type="app")
            add_edge(cmd, "opens", app)
            if intent:
                add_edge(intent, "uses_app", app)
        url = step.get("url") or ""
        if url:
            site = _extract_site(url)
            if site:
                add_node(site, node_type="site")
                add_edge(cmd, "visits", site)
        path = step.get("path") or step.get("filename") or ""
        if path:
            add_node(path, node_type="file")
            add_edge(cmd, "creates_file", path)
        if outcome == "failure" and action:
            add_edge(cmd, "failed_at", action, weight=0.5)
        elif outcome == "success" and action:
            add_edge(cmd, "succeeded_with", action, weight=1.0)


def _extract_intent(plan):
    if not plan:
        return ""
    if isinstance(plan, dict) and "workflow" in plan:
        steps = plan.get("workflow", [])
        if steps and isinstance(steps[0], dict):
            return steps[0].get("action") or steps[0].get("intent") or ""
    if isinstance(plan, list) and plan:
        if isinstance(plan[0], dict):
            return plan[0].get("intent") or ""
    return ""


def _extract_site(url):
    for site in ["youtube", "google", "github", "stackoverflow", "twitter"]:
        if site in url:
            return site
    return ""


def what_does_fury_know_about(concept):
    related = get_related(concept)
    if not related:
        print(f"Fury knows nothing about '{concept}' yet.")
        return
    print(f"\n--- Fury knows about '{concept}' ---")
    for item in related.get("knows", []):
        print(f"  {concept} --[{item['relation']}]--> {item['target']}  (w={item['weight']})")
    for item in related.get("known_by", []):
        print(f"  {item['source']} --[{item['relation']}]--> {concept}  (w={item['weight']})")
    print("---\n")


def top_nodes(node_type=None, limit=5):
    try:
        conn = _get_conn()
        if node_type:
            rows = conn.execute(
                "SELECT name, count FROM kg_nodes WHERE node_type=? "
                "ORDER BY count DESC LIMIT ?", (node_type, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT name, count FROM kg_nodes ORDER BY count DESC LIMIT ?",
                (limit,)
            ).fetchall()
        conn.close()
        return [{"name": r[0], "count": r[1]} for r in rows]
    except:
        return []