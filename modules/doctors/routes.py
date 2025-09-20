# modules/doctors/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.core.db import get_db
from modules.auth.security import get_current_user
from modules.users.models import User
from modules.doctors import crud, schemas

router = APIRouter(prefix="/doctors", tags=["doctors"])

@router.post("/me", response_model=schemas.DoctorOut)
def create_or_update_doc_profile(payload: schemas.DoctorCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can create a doctor profile")
    existing = crud.get_doctor_by_user_id(db, current_user.id)
    if existing:
        # simple update
        existing.specialization = payload.specialization or existing.specialization
        existing.qualifications = payload.qualifications or existing.qualifications
        existing.bio = payload.bio or existing.bio
        db.commit()
        db.refresh(existing)
        return existing
    new = crud.create_doctor_profile(db, current_user.id, payload.specialization, payload.qualifications, payload.bio)
    return new

@router.post("/me/slots", response_model=schemas.SlotOut)
def create_slot(slot: schemas.SlotCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors")
    doctor = crud.get_doctor_by_user_id(db, current_user.id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    new_slot = crud.create_slot(db, doctor.id, slot.start_datetime, slot.end_datetime)
    return new_slot

@router.get("/me/slots", response_model=list[schemas.SlotOut])
def list_my_available_slots(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors")
    doctor = crud.get_doctor_by_user_id(db, current_user.id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    return crud.get_available_slots(db, doctor.id)

@router.post("/me/slots-range", response_model=list[schemas.SlotOut])
def create_slots_range(payload: schemas.SlotRangeCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors")
    doctor = crud.get_doctor_by_user_id(db, current_user.id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    slots = crud.create_slots_range(db, doctor.id, payload.start_datetime, payload.end_datetime)
    return slots
