from sqlalchemy import Column, Integer, String
from app.database import Base # Absolute import

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    description = Column(String)
    required_skills = Column(String) # We will store skills like "Python, SQL, React"