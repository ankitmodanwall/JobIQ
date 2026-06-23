import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Salary Service")

class SalaryRequest(BaseModel):
    experience: float
    role: str = "Engineer"

@app.get("/")
def home():
    return {"status": "Salary Service Online"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "salary-service"}

@app.post("/predict-salary")
def predict(data: SalaryRequest):
    # Simple salary calculation
    base = 50000 + (data.experience * 15000)
    
    role_multiplier = {
        "engineer": 1.0,
        "senior engineer": 1.3,
        "lead": 1.5,
        "manager": 1.6,
        "director": 2.0,
        "ai engineer": 1.4,
        "data scientist": 1.35,
        "ml engineer": 1.45
    }
    
    multiplier = role_multiplier.get(data.role.lower(), 1.0)
    final_salary = base * multiplier
    
    return {
        "experience": data.experience,
        "role": data.role,
        "predicted_salary_lpa": round(final_salary, 2)
    }