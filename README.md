# Job Intelligence Platform - Setup & Running Guide

## Overview
This is a microservices-based AI job intelligence platform with:
- **API Gateway** (Port 8000) - Main entry point
- **User Service** (Port 8001) - Authentication & user management
- **Resume Service** (Port 8002) - Resume parsing & analysis
- **Job Service** (Port 8003) - Job listings & management
- **Match Service** (Port 8004) - Job-resume matching
- **Salary Service** (Port 8005) - Salary predictions
- **Interview Service** (Port 8006) - Interview question generation
- **Frontend** (Port 5173) - React-based UI
- **Database** (PostgreSQL on 5432)
- **Cache** (Redis on 6379)
- **Message Queue** (Kafka on 9092)

## Prerequisites
- Python 3.8+
- Node.js 16+
- Docker & Docker Compose (optional, for databases)

## Quick Start

### 1. Start Backend Services

Open multiple terminal windows and run each service:

**Terminal 1 - API Gateway:**
```bash
cd backend/api-gateway
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 - User Service:**
```bash
cd backend/user-service
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

**Terminal 3 - Resume Service:**
```bash
cd backend/resume-service
python -m uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload
```

**Terminal 4 - Job Service:**
```bash
cd backend/job-service
python -m uvicorn app.main:app --host 127.0.0.1 --port 8003 --reload
```

**Terminal 5 - Salary Service:**
```bash
cd backend/salary-service
python -m uvicorn app.main:app --host 127.0.0.1 --port 8005 --reload
```

**Terminal 6 - Interview Service:**
```bash
cd backend/interview-service
python -m uvicorn app.main:app --host 127.0.0.1 --port 8006 --reload
```

### 2. Start Frontend

**Terminal 7 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Access Points
- **Frontend UI**: http://localhost:5173
- **API Gateway Docs**: http://localhost:8000/docs
- **User Service Docs**: http://localhost:8001/docs
- **Resume Service Docs**: http://localhost:8002/docs
- **Job Service Docs**: http://localhost:8003/docs
- **Salary Service Docs**: http://localhost:8005/docs
- **Interview Service Docs**: http://localhost:8006/docs

## Automated Startup (Windows)
Run the provided batch file:
```bash
start-all-services.bat
```

## Database Setup

### Using Docker Compose
```bash
docker-compose up -d
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Zookeeper (port 2181)
- Kafka (port 9092)

### Manual Setup
Ensure PostgreSQL and Redis are running on their default ports.

## Troubleshooting

### Port 8000 Already in Use
Kill the process on port 8000:
```powershell
Get-NetTCPConnection -LocalPort 8000 | Stop-Process -Force
```

### Module Not Found Errors
Ensure Python virtual environments are activated and dependencies installed:
```bash
# For each service directory:
python -m pip install -r requirements.txt
```

### Frontend Can't Connect to Backend
- Check that all backend services are running on localhost
- Verify API Gateway is accessible at http://localhost:8000/health
- Check browser console for CORS errors

## Project Structure
```
backend/
├── api-gateway/          # FastAPI gateway
├── user-service/         # User authentication & management
├── resume-service/       # Resume parsing & NLP
├── job-service/          # Job management
├── salary-service/       # ML-based salary prediction
├── interview-service/    # Interview question generation
└── recommendation-service/

frontend/
├── src/
│   ├── pages/           # Page components
│   ├── components/      # Reusable components
│   ├── services/        # API service layers
│   └── App.jsx
└── package.json
```

## Key Features Implemented
- ✅ User authentication (Login/Register)
- ✅ Resume upload & parsing
- ✅ Job matching with skills
- ✅ Salary prediction
- ✅ Interview question generation
- ✅ Dashboard with AI insights

## API Endpoints

### Authentication
- `POST /users/login` - Login
- `POST /users/` - Register
- `GET /users/{user_id}` - Get user

### Resume
- `POST /upload-resume/` - Upload resume file

### Reports
- `POST /full-report` - Get combined analysis (match, salary, interview)

## Environment Variables
See `.env` files in each service directory for configuration.

## Notes
- All services use localhost for inter-service communication
- CORS is enabled on API Gateway to allow frontend connections
- Database operations use SQLAlchemy ORM
- Redis is used for caching
- Kafka is used for event streaming

For detailed service documentation, check individual service README files.
