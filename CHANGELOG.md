# Changelog

All notable changes to Fury are documented here.
Format: `[version] — date — description`

---

## [1.0.0] — 2026-04-13 — First public release

### Phase 9B — Community packaging
- One-click Windows installer (`install.bat`)
- Config system (`config.yaml` + `.env.template`)
- Web dashboard (FastAPI + React) with 6 tabs
- Skill export/import system
- Safety sandbox — blocks dangerous commands
- Permission system — per-capability user consent
- GitHub Actions CI — auto tests on push
- Full test suite (16 tests)

### Phase 9A — Smarter reasoning
- Chain-of-thought reasoning (`thinking_engine_v2.py`)
- Multi-hypothesis planning (`planner_v2.py`)
- Self-reflection after every action (`reflection_engine.py`)
- Semantic vision — understands screen content (`vision_understanding.py`)
- Curiosity engine — asks before acting on unclear commands
- Confidence scoring — knows when it's uncertain
- Episodic memory — rich session history in SQLite
- Knowledge graph — builds connected knowledge over time
- Pattern recognizer — detects behavioral templates
- Intent predictor — suggests next commands

### Phase 8 — Intelligence layer (Steps 107–110)
- Context engine — understands vague commands
- Failure memory — learns from mistakes
- Personality — consistent assistant feel
- Speed optimization — direct URL search

### Phase 7 — Computer operator (Steps 91–106)
- Full UI action engine
- UI planner and operator loop
- App intelligence agent
- Multi-app agent
- Navigation engine
- Screen memory

### Phase 6 — Autonomous AI brain (Steps 76–90)
- Task understanding engine
- Hierarchical planner
- Knowledge database
- Code analyzer
- Thinking, decision, and strategy engines
- Experience memory

### Phase 5 — Self-improving core (Steps 61–75)
- Memory database (SQLite)
- Skill database
- Session database
- Self-improve loop
- Graph planner

### Phase 4 — Multi-agent system (Steps 41–60)
- 30+ specialized agents
- Agent registry and controller
- Base agent architecture
- Central routing

### Phase 3 — Jarvis / Voice (Steps 26–40)
- Goal engine
- Auto loop
- Speech to text
- Text to speech
- Screen capture + OCR
- UI click engine

### Phase 2 — Workflow engine (Steps 11–25)
- Multi-step command execution
- Task planner
- Window manager
- Browser agent
- Typing engine

### Phase 1 — Foundation (Steps 1–10)
- Basic text command pipeline
- `fury.py` entry point
- Command parser
- Skill manager + registry
- UI engine
- File manager
- Software control
- Can open apps, type text, create files, run terminal commands

---

## Roadmap

### [1.1.0] — Phase 10 — Human-level PC operator
- Visual agent loop (see → decide → act → verify)
- Task memory (mid-task state recovery)
- Goal decomposer
- Tab intelligence (finds accounts in open tabs)
- LeetCode solver agent
- WhatsApp automation agent
- Telegram automation agent
- Job application agent
- YouTube play agent (not just search)
- Movie finder agent
- Gmail full agent
- LinkedIn agent
- Multi-language project builder

### [1.2.0] — Phase 11 — Mobile + cloud
- Mobile control app
- Remote headless mode
- Plugin marketplace