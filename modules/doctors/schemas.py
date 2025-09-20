# modules/doctors/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DoctorCreate(BaseModel):
    specialization: Optional[str]
    qualifications: Optional[str]
    bio: Optional[str]

class SlotCreate(BaseModel):
    start_datetime: datetime
    end_datetime: datetime

class DoctorOut(BaseModel):
    id: int
    user_id: int
    specialization: Optional[str]
    qualifications: Optional[str]
    bio: Optional[str]
    class Config:
        orm_mode = True

class SlotOut(BaseModel):
    id: int
    doctor_id: int
    start_datetime: datetime
    end_datetime: datetime
    is_booked: bool
    
    model_config = {"from_attributes": True}

class SlotRangeCreate(BaseModel):
    start_datetime: datetime
    end_datetime: datetime