from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os

from app.parser.resume_parser import extract_text_from_pdf
from app.database import Base, engine, get_db
from app.models import Resume
from app.kafka_producer import send_resume_event

# ✅ CREATE APP OBJECT
app = FastAPI(title="Resume Service")

# Create database tables
Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "resume-service"}


@app.post("/upload-resume")
async def upload_resume(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # ✅ Ensure filename is string
        filename = str(file.filename) if file.filename else "unknown.pdf"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = extract_text_from_pdf(file_path)

        new_resume = Resume(
            user_id=user_id,
            filename=filename,
            extracted_text=extracted_text
        )

        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)

        send_resume_event({
            "resume_id": new_resume.id,
            "user_id": new_resume.user_id,
            "filename": new_resume.filename
        })

        return {
            "message": "Resume uploaded successfully",
            "resume_id": new_resume.id,
            "user_id": new_resume.user_id,
            "filename": new_resume.filename,
            "characters": len(extracted_text)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/resumes/")
def get_all_resumes(db: Session = Depends(get_db)):
    resumes = db.query(Resume).all()
    return resumes


@app.get("/resumes/{resume_id}")
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume