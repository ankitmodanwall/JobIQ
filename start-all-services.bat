@echo off
REM Start all backend services in separate windows

echo Starting API Gateway on port 8000...
start "API Gateway" cmd /k "cd d:\JOB-INTELLIGENCE-PLATFORM\backend\api-gateway && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3

echo Starting User Service on port 8001...
start "User Service" cmd /k "cd d:\JOB-INTELLIGENCE-PLATFORM\backend\user-service && python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload"

timeout /t 3

echo Starting Resume Service on port 8002...
start "Resume Service" cmd /k "cd d:\JOB-INTELLIGENCE-PLATFORM\backend\resume-service && python -m uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload"

timeout /t 3

echo Starting Job Service on port 8003...
start "Job Service" cmd /k "cd d:\JOB-INTELLIGENCE-PLATFORM\backend\job-service && python -m uvicorn app.main:app --host 127.0.0.1 --port 8003 --reload"

timeout /t 3

echo Starting Salary Service on port 8005...
start "Salary Service" cmd /k "cd d:\JOB-INTELLIGENCE-PLATFORM\backend\salary-service && python -m uvicorn app.main:app --host 127.0.0.1 --port 8005 --reload"

timeout /t 3

echo Starting Interview Service on port 8006...
start "Interview Service" cmd /k "cd d:\JOB-INTELLIGENCE-PLATFORM\backend\interview-service && python -m uvicorn app.main:app --host 127.0.0.1 --port 8006 --reload"

timeout /t 3

echo Starting Frontend on port 5173...
start "Frontend" cmd /k "cd d:\JOB-INTELLIGENCE-PLATFORM\frontend && npm install && npm run dev"

echo All services started! Check the individual windows for logs.
echo API Gateway: http://localhost:8000
echo Frontend: http://localhost:5173
