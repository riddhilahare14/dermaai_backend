# modules/infections/models.py
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from modules.core.db import Base
import datetime

class InfectionRecord(Base):
    __tablename__ = "infection_records"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String, nullable=False)
    ai_response = Column(JSON, nullable=True)  # JSON dump as text
    diagnosis = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    recommended_consultation = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    patient = relationship("Patient")
