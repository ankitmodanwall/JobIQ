from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, database, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Job Service")


@app.get("/")
def home():
    return {
        "message": "Job Service is Online"
    }


@app.post("/jobs/", response_model=schemas.JobResponse)
def add_job(
    job: schemas.JobCreate,
    db: Session = Depends(database.get_db)
):
    new_job = models.Job(
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        required_skills=job.required_skills
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


@app.get("/jobs/")
def get_jobs(
    db: Session = Depends(database.get_db)
):
    return db.query(models.Job).all()


@app.get("/jobs/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(database.get_db)
):
    job = (
        db.query(models.Job)
        .filter(models.Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job