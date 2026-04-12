# Contributing to Fury

Thanks for your interest in contributing! Fury is an autonomous AI desktop assistant and there's a lot of room to add new skills, agents, and capabilities.

---

## Ways to contribute

- **Add a new skill** — teach Fury how to do something new
- **Add a new agent** — specialized agent for a platform (WhatsApp, LeetCode, etc.)
- **Fix a bug** — check the Issues tab for open bugs
- **Improve parsing** — add patterns to `command_parser.py`
- **Write tests** — add to `backend/tests/`
- **Improve docs** — fix README, add examples

---

## Getting started

```bash
# 1. Fork the repo on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/fury-automation-assistant.git
cd fury-automation-assistant

# 3. Install dependencies
install.bat

# 4. Add your API key
copy backend\.env.template backend\.env
# edit backend\.env and add GROQ_API_KEY

# 5. Run Fury
cd backend
python fury.py
```

---

## Adding a new skill

Skills live in `backend/skills/skills_registry.py`. To add one:

**1. Write the skill function:**
```python
def skill_my_new_skill(task):
    # task is a dict with intent + any fields you define
    name = task.get("name")
    if name:
        # do something
        memory.set_action("my_new_skill")
        return True
```

**2. Register it in the SKILLS dict:**
```python
SKILLS = {
    ...
    "my_new_skill": skill_my_new_skill,
}
```

**3. Add parsing in `command_parser.py`:**
```python
if "my trigger phrase" in command:
    return _attach_raw({
        "intent": "my_new_skill",
        "name": command.replace("my trigger phrase", "").strip(),
    }, original)
```

**4. Test it:**
```bash
cd backend
python fury.py
>>> my trigger phrase hello
```

---

## Adding a new agent

Agents live in `backend/agents/`. To add one:

```python
# agents/my_agent.py
from agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("MyAgent")

    def can_handle(self, task):
        if not isinstance(task, dict):
            return False
        return task.get("intent") == "my_intent"

    def handle(self, task):
        print("MyAgent handling:", task)
        # do something
        return None
```

Then register it in `backend/agents/register_agents.py`:
```python
from agents.my_agent import MyAgent
registry.register(MyAgent())
```

---

## Code style

- Python 3.10+
- No external formatters required — just keep it readable
- snake_case for functions and variables
- Docstrings on public functions
- Print statements for debug output (Fury uses these intentionally)

---

## Pull request process

1. Create a branch: `git checkout -b feature/my-skill`
2. Make your changes
3. Run tests: `cd backend && pytest tests/ -v`
4. Commit: `git commit -m "add: my skill description"`
5. Push: `git push origin feature/my-skill`
6. Open a Pull Request on GitHub

**Commit message format:**
```
add: new whatsapp skill
fix: command parser typo handling
improve: reflection engine accuracy
docs: update README examples
test: add parser tests
```

---

## Issue templates

When opening an issue please include:

**Bug report:**
- What command did you run?
- What did you expect?
- What actually happened?
- Paste the terminal output

**Feature request:**
- What do you want Fury to do?
- Example command you'd type
- Any ideas on implementation?

---

## Questions?

Open a GitHub Discussion or an Issue tagged `question`.