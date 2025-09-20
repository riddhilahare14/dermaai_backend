# modules/patients/models.py
from sqlalchemy import Column, Integer, String, Date, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from modules.core.db import Base
import datetime

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    dob = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    medical_history = Column(JSON, nullable=True)
    profile_image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="patient")
