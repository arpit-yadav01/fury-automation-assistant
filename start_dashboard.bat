@echo off
echo.
echo  ==========================================
echo   FURY DASHBOARD — STARTING
echo  ==========================================
echo.

:: Start FastAPI in background
echo  Starting Fury API on http://localhost:8000 ...
start "Fury API" cmd /k "cd backend && uvicorn dashboard_api:app --reload --port 8000"

:: Wait 2 seconds
timeout /t 2 /nobreak >nul

:: Start React frontend
echo  Starting Fury Dashboard on http://localhost:3000 ...
start "Fury Dashboard" cmd /k "cd frontend && npm start"

echo.
echo  Dashboard will open at http://localhost:3000
echo  API running at http://localhost:8000
echo  API docs at http://localhost:8000/docs
echo.