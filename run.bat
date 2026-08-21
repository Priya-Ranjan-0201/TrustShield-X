@echo off
title TruthShield X — Unified Stack Launcher
color 0A

echo ================================================================================
echo                   TRUTHSHIELD X — UNIFIED STACK LAUNCHER
echo                 Release: REL-4.0.0-PROD-CERTIFIED
echo ================================================================================
echo.

cd /d "%~dp0"

echo [1/4] Starting PostgreSQL and Redis Docker services...
docker-compose up -d postgres redis
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Docker services could not be started or are already running. Continuing...
)
echo.

echo [2/4] Applying Database Migrations and Initializing Demo Accounts...

cd /d "%~dp0backend\auth-service"
uv run alembic upgrade head
cd /d "%~dp0"
uv run python scripts\seed_demo_accounts.py >nul 2>&1
echo.

echo [3/4] Launching Backend FastAPI Server on http://127.0.0.1:8000 ...
start "TruthShield X — Backend API (Port 8000)" cmd /k "cd /d "%~dp0backend\auth-service" && color 0B && title Backend API [Port 8000] && uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [4/4] Launching Frontend React Web Console on http://127.0.0.1:5180 ...
start "TruthShield X — Frontend Web (Port 5180)" cmd /k "cd /d "%~dp0apps\web" && color 0D && title Frontend Web [Port 5180] && npm run dev"

echo.
echo ================================================================================
echo                     ALL SERVICES LAUNCHED SUCCESSFULLY!
echo ================================================================================
echo.
echo   * Frontend Web Console:    http://localhost:5180
echo   * Backend REST API:        http://127.0.0.1:8000
echo   * Interactive Swagger UI:  http://127.0.0.1:8000/api/v1/docs
echo   * ReDoc API Reference:     http://127.0.0.1:8000/api/v1/redoc

echo.
echo --------------------------------------------------------------------------------
echo   DEMO CREDENTIALS (Pre-Configured):
echo --------------------------------------------------------------------------------
echo   1. Administrator (Full SecOps Access):
echo      Email:    admin@truthshield.com
echo      Password: AdminPassword123!
echo.
echo   2. Lead Analyst (SOC / Threat Intel / Copilot):
echo      Email:    analyst@truthshield.com
echo      Password: AnalystPassword123!
echo.
echo   3. Citizen / Demo User (Multi-Modal Scanner):
echo      Email:    demo@truthshield.com
echo      Password: DemoPassword123!
echo --------------------------------------------------------------------------------
echo.
echo Keep the backend and frontend terminal windows open while working.
echo ================================================================================
echo.

timeout /t 3 >nul
start http://localhost:5180

exit /b 0


