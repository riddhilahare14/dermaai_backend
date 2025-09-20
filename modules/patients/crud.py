# modules/patients/crud.py
from sqlalchemy.orm import Session
from modules.patients.models import Patient
from datetime import date

def create_patient(db: Session, user_id: int, dob: date | None = None, gender: str | None = None, medical_history: str | None = None, profile_image: str | None = None):
    patient = Patient(user_id=user_id, dob=dob, gender=gender, medical_history=medical_history, profile_image=profile_image)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def get_patient_by_user_id(db: Session, user_id: int):
    return db.query(Patient).filter(Patient.user_id == user_id).first()

def update_patient(db: Session, user_id: int, **updates):
    patient = get_patient_by_user_id(db, user_id)
    if not patient:
        return None
    for k, v in updates.items():
        setattr(patient, k, v)
    db.commit()
    db.refresh(patient)
    return patient
