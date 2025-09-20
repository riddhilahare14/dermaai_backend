# modules/patients/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class PatientCreate(BaseModel):
    dob: Optional[date]
    gender: Optional[str]
    medical_history: Optional[list[str]]
    profile_image: Optional[str]

class PatientOut(BaseModel):
    id: int
    user_id: int
    dob: Optional[date]
    gender: Optional[str]
    medical_history: Optional[list[str]]
    profile_image: Optional[str]

    model_config = {"from_attributes": True}

