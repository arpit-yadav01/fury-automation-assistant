@echo off
echo.
echo  ==========================================
echo   FURY AI ASSISTANT — INSTALLER
echo  ==========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found.
    echo  Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo  [OK] Python found
echo.

:: Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] pip not found. Please reinstall Python with pip.
    pause
    exit /b 1
)

echo  [OK] pip found
echo.

:: Install dependencies
echo  Installing dependencies...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo  [ERROR] Dependency installation failed.
    echo  Check requirements.txt and try again.
    pause
    exit /b 1
)

echo.
echo  [OK] Dependencies installed
echo.

:: Create memory folder
if not exist "backend\memory" (
    mkdir backend\memory
    echo  [OK] Created memory folder
)

:: Create .env from template if not exists
if not exist "backend\.env" (
    if exist "backend\.env.template" (
        copy backend\.env.template backend\.env >nul
        echo  [OK] Created .env from template
        echo.
        echo  !! IMPORTANT: Open backend\.env and add your API keys
        echo.
    ) else (
        echo  [WARN] No .env.template found — skipping .env creation
    )
) else (
    echo  [OK] .env already exists
)

:: Create config.yaml from template if not exists
if not exist "backend\config.yaml" (
    if exist "backend\config.template.yaml" (
        copy backend\config.template.yaml backend\config.yaml >nul
        echo  [OK] Created config.yaml from template
    )
) else (
    echo  [OK] config.yaml already exists
)

echo.
echo  ==========================================
echo   FURY INSTALLED SUCCESSFULLY
echo  ==========================================
echo.
echo  Next steps:
echo   1. Open backend\.env and add your GROQ_API_KEY
echo   2. Run: cd backend ^&^& python fury.py
echo.
pause