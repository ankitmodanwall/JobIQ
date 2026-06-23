from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI(title="Recommendation Service")


class MatchRequest(BaseModel):
    user_skills: List[str]
    job_skills: str


@app.get("/")
def home():
    return {
        "message": "Recommendation Engine is Online"
    }


@app.post("/match/")
def match_skills(data: MatchRequest):

    user_set = set(
        [skill.lower().strip()
         for skill in data.user_skills]
    )

    job_set = set(
        [skill.lower().strip()
         for skill in data.job_skills.split(",")]
    )

    matched_skills = user_set.intersection(job_set)

    missing_skills = job_set - user_set

    score = (
        len(matched_skills) / len(job_set)
    ) * 100 if job_set else 0

    return {
        "match_score": round(score, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "verdict":
            "Great Match!"
            if score >= 60
            else "Skill Gap Detected"
    }