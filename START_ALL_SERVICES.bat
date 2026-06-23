@echo off
REM ==========================================
REM  JOB INTELLIGENCE PLATFORM - AUTO STARTUP
REM ==========================================

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  JOB INTELLIGENCE PLATFORM - STARTUP SCRIPT                ║
echo ║  This will start ALL services in separate windows          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Node.js not found. Please install Node.js 16+
    pause
    exit /b 1
)

echo ✅ Python and Node.js detected
echo.
echo Starting services... (7 windows will open)
echo.

REM Create a temporary batch file for each service
cd /d "d:\JOB-INTELLIGENCE-PLATFORM"

REM API Gateway
echo [1/7] Starting API Gateway (Port 8000)...
start "API Gateway - 8000" cmd /k "cd backend\api-gateway && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
timeout /t 2 /nobreak

REM User Service
echo [2/7] Starting User Service (Port 8001)...
start "User Service - 8001" cmd /k "cd backend\user-service && python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload"
timeout /t 2 /nobreak

REM Resume Service
echo [3/7] Starting Resume Service (Port 8002)...
start "Resume Service - 8002" cmd /k "cd backend\resume-service && python -m uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload"
timeout /t 2 /nobreak

REM Job Service
echo [4/7] Starting Job Service (Port 8003)...
start "Job Service - 8003" cmd /k "cd backend\job-service && python -m uvicorn app.main:app --host 127.0.0.1 --port 8003 --reload"
timeout /t 2 /nobreak

REM Salary Service
echo [5/7] Starting Salary Service (Port 8005)...
start "Salary Service - 8005" cmd /k "cd backend\salary-service && python -m uvicorn app.main:app --host 127.0.0.1 --port 8005 --reload"
timeout /t 2 /nobreak

REM Interview Service
echo [6/7] Starting Interview Service (Port 8006)...
start "Interview Service - 8006" cmd /k "cd backend\interview-service && python -m uvicorn app.main:app --host 127.0.0.1 --port 8006 --reload"
timeout /t 2 /nobreak

REM Frontend
echo [7/7] Starting Frontend (Port 5173)...
start "Frontend - 5173" cmd /k "cd frontend && npm run dev"
timeout /t 3 /nobreak

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  ✅ ALL SERVICES STARTED!                                  ║
echo ╠════════════════════════════════════════════════════════════╣
echo ║  Service              Port    URL                          ║
echo ║  ─────────────────────────────────────────────────────────  ║
echo ║  API Gateway          8000    http://localhost:8000        ║
echo ║  User Service         8001    http://localhost:8001        ║
echo ║  Resume Service       8002    http://localhost:8002        ║
echo ║  Job Service          8003    http://localhost:8003        ║
echo ║  Salary Service       8005    http://localhost:8005        ║
echo ║  Interview Service    8006    http://localhost:8006        ║
echo ║  Frontend             5173    http://localhost:5173        ║
echo ╠════════════════════════════════════════════════════════════╣
echo ║  NEXT STEPS:                                               ║
echo ║  1. Wait for "Application startup complete" in each window ║
echo ║  2. Open http://localhost:5173 in your browser             ║
echo ║  3. Register and start using the platform!                 ║
echo ║                                                            ║
echo ║  📖 Read STARTUP_GUIDE.md for detailed instructions         ║
echo ║  📋 Read QUICK_REFERENCE.md for API endpoints               ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
