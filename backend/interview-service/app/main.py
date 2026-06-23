from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sys
import os

# This line forces Python to look in the current folder for the generator
sys.path.append(os.path.dirname(__file__))

try:
    from generator.question_generator import generate_questions
except ImportError:
    from app.generator.question_generator import generate_questions

app = FastAPI(title="Interview Service")

class InterviewRequest(BaseModel):
    role: str
    skills: List[str]

@app.get("/")
def home():
    return {"status": "Interview Service is Online"}

@app.post("/generate-questions")
def get_prep(data: InterviewRequest):
    questions = generate_questions(data.role, data.skills)
    return {
        "role": data.role,
        "suggested_questions": questions
    }