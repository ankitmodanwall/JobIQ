# 🚀 COMPLETE SETUP & EXECUTION GUIDE

## STEP 1: PREREQUISITES SETUP (DO THIS ONCE)

### Install Python Dependencies for Each Backend Service

Open PowerShell and run:

```powershell
# Go to each service and install dependencies

cd "d:\JOB-INTELLIGENCE-PLATFORM\backend\api-gateway"
pip install -r requirements.txt

cd "d:\JOB-INTELLIGENCE-PLATFORM\backend\user-service"
pip install -r requirements.txt

cd "d:\JOB-INTELLIGENCE-PLATFORM\backend\resume-service"
pip install -r requirements.txt

cd "d:\JOB-INTELLIGENCE-PLATFORM\backend\job-service"
pip install -r requirements.txt

cd "d:\JOB-INTELLIGENCE-PLATFORM\backend\salary-service"
pip install -r requirements.txt

cd "d:\JOB-INTELLIGENCE-PLATFORM\backend\interview-service"
pip install -r requirements.txt
```

### Install Frontend Dependencies

```powershell
cd "d:\JOB-INTELLIGENCE-PLATFORM\frontend"
npm install
```

---

## STEP 2: START ALL SERVICES (THE MAIN STEP)

**Open 7 different PowerShell/Terminal windows. In each, paste and run:**

### Window 1 - API Gateway (PORT 8000)
```powershell
cd "d:\JOB-INTELLIGENCE-PLATFORM\backend\api-gateway"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
✅ Wait for: `Application startup complete`

### Window 2 - User Service (PORT 8001)
```powershell
cd "d:\JOB-INTELLIGENCE-PLATFORM\backend\user-service"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```
✅ Wait for: `Application startup complete`

### Window 3 - Resume Service (PORT 8002)
```powershell
cd "d:\JOB-INTELLIGENCE-PLATFORM\backend\resume-service"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload
```
✅ Wait for: `Application startup complete`

### Window 4 - Job Service (PORT 8003)
```powershell
cd "d:\JOB-INTELLIGENCE-PLATFORM\backend\job-service"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8003 --reload
```
✅ Wait for: `Application startup complete`

### Window 5 - Salary Service (PORT 8005)
```powershell
cd "d:\JOB-INTELLIGENCE-PLATFORM\backend\salary-service"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8005 --reload
```
✅ Wait for: `Application startup complete`

### Window 6 - Interview Service (PORT 8006)
```powershell
cd "d:\JOB-INTELLIGENCE-PLATFORM\backend\interview-service"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8006 --reload
```
✅ Wait for: `Application startup complete`

### Window 7 - Frontend (PORT 5173)
```powershell
cd "d:\JOB-INTELLIGENCE-PLATFORM\frontend"
npm run dev
```
✅ Wait for: `➜  Local: http://localhost:5173/`

---

## STEP 3: VERIFY EVERYTHING IS RUNNING

Open your browser and check these URLs:

| Service | URL | Expected |
|---------|-----|----------|
| **Frontend** | http://localhost:5173 | Home page with login button |
| **API Gateway Health** | http://localhost:8000/health | `{"status":"API Gateway is running"}` |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **User Service** | http://localhost:8001/docs | User service endpoints |

---

## STEP 4: TEST THE APPLICATION

### 4.1 Create an Account
1. Open http://localhost:5173
2. Click "Sign In" button
3. Click "Sign Up" tab
4. Enter:
   - **Full Name**: Your Name
   - **Email**: test@example.com
   - **Password**: password123
5. Click "Register Now"

### 4.2 Upload Resume
1. After login, click "Resume" in sidebar
2. Select a PDF or Word document
3. Click "Upload Resume"

### 4.3 View Career Analysis
1. Click "Dashboard" in sidebar
2. Click "Generate AI Report" button
3. Wait for analysis results:
   - Match Score
   - Market Salary
   - Interview Prep Questions

### 4.4 Explore Other Features
- **Salary Predictor**: Adjust experience level and role
- **Job Listings**: View available opportunities
- **Interview Prep**: Practice interview questions

---

## TROUBLESHOOTING

### ❌ "Port 8000 already in use"
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue).OwningProcess | Stop-Process -Force
```

### ❌ "Module not found" error
```powershell
cd d:\JOB-INTELLIGENCE-PLATFORM\backend\[service-name]
pip install -r requirements.txt
```

### ❌ Frontend shows "Backend Port 8000 is not responding"
- Ensure API Gateway is running in Window 1
- Check http://localhost:8000/health returns status

### ❌ "Cannot import module"
- Make sure you're in the correct service directory
- Check Python version: `python --version` (should be 3.8+)

### ❌ npm install fails
```powershell
cd d:\JOB-INTELLIGENCE-PLATFORM\frontend
npm cache clean --force
npm install
```

---

## QUICK REFERENCE - SERVICE PORTS

```
API Gateway:     http://localhost:8000  (Main entry point)
User Service:    http://localhost:8001
Resume Service:  http://localhost:8002
Job Service:     http://localhost:8003
Salary Service:  http://localhost:8005
Interview Svc:   http://localhost:8006
Frontend:        http://localhost:5173
PostgreSQL DB:   localhost:5432
Redis Cache:     localhost:6379
```

---

## API ENDPOINTS FOR TESTING

### Authentication
```bash
POST http://localhost:8000/users/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}
```

### Resume Upload
```bash
POST http://localhost:8000/upload-resume/
(multipart form-data with file)
```

### Get AI Report
```bash
POST http://localhost:8000/full-report
Content-Type: application/json

{
  "user_skills": ["Python", "SQL", "React"],
  "job_title": "Software Engineer",
  "job_skills": "Python, SQL, Docker, FastAPI",
  "experience": 3
}
```

### Get Salary Estimate
```bash
GET http://localhost:8000/estimate-salary?exp=3&role=Engineer
```

---

## NEXT STEPS FOR DEVELOPMENT

1. **Database Setup**: Run Docker Compose for PostgreSQL, Redis, Kafka
   ```powershell
   docker-compose up -d
   ```

2. **Add More Features**:
   - Integrate more AI models in each service
   - Add user profile management
   - Implement job alerts
   - Add social features

3. **Deploy to Production**:
   - Use Docker containers for all services
   - Set up Kubernetes clusters
   - Use cloud databases (AWS RDS, Azure Cosmos)

4. **Performance Optimization**:
   - Add caching layers with Redis
   - Implement job queuing with Kafka
   - Add API rate limiting

---

## IMPORTANT FILES FIXED

✅ `frontend/src/services/api.js` - Added missing `getFullReport` method
✅ `frontend/src/services/jobService.js` - Added `getAll()` method
✅ `frontend/src/pages/ResumeUpload.jsx` - Fixed to actual resume upload page
✅ `frontend/src/pages/SalaryPredictor.jsx` - Fixed to use service layer
✅ `frontend/src/App.jsx` - Added missing routes for Salary & Interview pages
✅ `backend/api-gateway/app/main.py` - Added missing endpoints

---

**Everything is now connected and ready to run! Follow STEP 2 to start all services.** 🎉
