# modules/appointments/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AppointmentRequest(BaseModel):
    infection_record_id: Optional[int] = None  # optional reference to infection result
    preferred_specialization: Optional[str] = None  # optional filter

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    slot_id: int
    status: str
    scheduled_at: datetime

    model_config = {"from_attributes": True}

