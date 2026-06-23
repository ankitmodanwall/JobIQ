import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx

load_dotenv()

app = FastAPI(title="AI Job Platform Gateway")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs from .env
SERVICES = {
    "user": os.getenv("USER_SERVICE_URL", "http://user_service:8001"),
    "resume": os.getenv("RESUME_SERVICE_URL", "http://resume_service:8002"),
    "job": os.getenv("JOB_SERVICE_URL", "http://job_service:8003"),
    "match": os.getenv("MATCH_SERVICE_URL", "http://match_service:8004"),
    "salary": os.getenv("SALARY_SERVICE_URL", "http://salary_service:8005"),
    "interview": os.getenv("INTERVIEW_SERVICE_URL", "http://interview_service:8006")
}

# ==================== HEALTH CHECK ====================
@app.get("/health")
def health_check():
    return {"status": "API Gateway is running"}

# ==================== USER SERVICE ENDPOINTS ====================

# ✅ Login endpoint (frontend calls this) - SIRF EK BAAR
@app.post("/login")
async def login(data: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{SERVICES['user']}/login", json=data)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"User Service Offline: {str(e)}")

# ✅ Register endpoint
@app.post("/users/")
async def register(data: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{SERVICES['user']}/users/", json=data)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"User Service Offline: {str(e)}")

# ✅ Get user by ID
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SERVICES['user']}/users/{user_id}")
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"User Service Offline: {str(e)}")

# ✅ Get all users
@app.get("/users/")
async def get_all_users():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SERVICES['user']}/users/")
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"User Service Offline: {str(e)}")

# ==================== RESUME SERVICE ENDPOINTS ====================

@app.post("/upload-resume/")
async def upload_to_resume_service(file: UploadFile = File(...)):
    async with httpx.AsyncClient() as client:
        try:
            files = {'file': (file.filename, file.file, file.content_type)}
            response = await client.post(f"{SERVICES['resume']}/upload-resume/", files=files)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Resume Service Offline: {str(e)}")

# ==================== JOB SERVICE ENDPOINTS ====================

@app.get("/get-jobs")
async def get_all_jobs():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SERVICES['job']}/jobs/")
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Job Service Offline: {str(e)}")

@app.get("/jobs")
async def get_jobs():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SERVICES['job']}/jobs/")
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Job Service Offline: {str(e)}")

# ==================== SALARY PREDICTION ENDPOINTS ====================

@app.get("/estimate-salary")
async def estimate_salary(exp: int = Query(0), role: str = Query("Engineer")):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{SERVICES['salary']}/predict-salary",
                json={"experience": exp, "role": role}
            )
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Salary Service Offline: {str(e)}")

# ==================== MATCH SERVICE ENDPOINTS ====================

@app.post("/match-resume/")
async def match_resume(data: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{SERVICES['match']}/match-resume/", json=data)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Match Service Offline: {str(e)}")

# ==================== INTERVIEW SERVICE ENDPOINTS ====================

@app.post("/generate-questions")
async def generate_questions(data: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{SERVICES['interview']}/generate-questions", json=data)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Interview Service Offline: {str(e)}")

# ==================== COMBINED REPORT ENDPOINT ====================

@app.post("/full-report")
async def get_combined_report(data: dict):
    async with httpx.AsyncClient() as client:
        try:
            match_response = await client.post(f"{SERVICES['match']}/match-resume/", json=data)
            salary_response = await client.post(f"{SERVICES['salary']}/predict-salary", json=data)
            interview_response = await client.post(f"{SERVICES['interview']}/generate-questions", json=data)

            return {
                "match_report": match_response.json(),
                "salary_prediction": salary_response.json(),
                "interview_questions": interview_response.json()
            }
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"One or more services are offline: {str(e)}")