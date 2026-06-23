from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    filename: str

    class Config:
        from_attributes = True