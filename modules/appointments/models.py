# modules/appointments/models.py
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, JSON
from sqlalchemy.orm import relationship
from modules.core.db import Base
import datetime

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    slot_id = Column(Integer, ForeignKey("doctor_slots.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    scheduled_at = Column(DateTime, nullable=False)

    # Agora-related fields
    channel_name = Column(String, nullable=True)
    agora_token = Column(String, nullable=True)

    patient = relationship("Patient")
    doctor = relationship("Doctor")
    slot = relationship("DoctorSlot")
