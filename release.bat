@echo off
echo.
echo  ==========================================
echo   FURY v1.0.0 — RELEASE
echo  ==========================================
echo.

:: Make sure we're on main
git checkout main

:: Pull latest
git pull origin main

:: Add all new files
git add .

:: Commit release
git commit -m "release: Fury v1.0.0 — Phase 9 complete"

:: Create tag
git tag -a v1.0.0 -m "Fury v1.0.0 — First public release

Phase 9 complete:
- 120+ steps built
- Chain-of-thought reasoning
- Multi-agent system (30+ agents)
- Self-improving memory
- Web dashboard
- Safety sandbox + permissions
- One-click installer
- GitHub Actions CI"

:: Push with tags
git push origin main --tags

echo.
echo  ==========================================
echo   RELEASED: v1.0.0
echo   Check: https://github.com/arpit-yadav01/fury-automation-assistant/releases
echo  ==========================================
echo.
pause