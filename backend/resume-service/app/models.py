from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    filename = Column(String(255))
    extracted_text = Column(Text)