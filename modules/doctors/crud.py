# modules/doctors/crud.py
from sqlalchemy.orm import Session
from modules.doctors.models import Doctor, DoctorSlot
from datetime import datetime, timedelta, timezone

def create_doctor_profile(db: Session, user_id: int, specialization: str | None = None, qualifications: str | None = None, bio: str | None = None):
    doc = Doctor(user_id=user_id, specialization=specialization, qualifications=qualifications, bio=bio)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def get_doctor_by_user_id(db: Session, user_id: int):
    return db.query(Doctor).filter(Doctor.user_id == user_id).first()

def create_slot(db: Session, doctor_id: int, start_datetime: datetime, end_datetime: datetime):
    # Convert incoming datetimes to UTC
    start_datetime_utc = start_datetime.astimezone(timezone.utc)
    end_datetime_utc = end_datetime.astimezone(timezone.utc)
    
    slot = DoctorSlot(
        doctor_id=doctor_id,
        start_datetime=start_datetime_utc,
        end_datetime=end_datetime_utc
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot

def create_slots_range(db: Session, doctor_id: int, start: datetime, end: datetime, slot_duration_minutes: int = 30):
    slots = []

    # Convert start and end to UTC
    current = start.astimezone(timezone.utc)
    end = end.astimezone(timezone.utc)

    while current < end:
        slot = DoctorSlot(
            doctor_id=doctor_id,
            start_datetime=current,
            end_datetime=current + timedelta(minutes=slot_duration_minutes),
            is_booked=False
        )
        db.add(slot)
        slots.append(slot)
        current += timedelta(minutes=slot_duration_minutes)
    db.commit()
    
    for slot in slots:
        db.refresh(slot)
    return slots

def get_available_slots(db: Session, doctor_id: int):
    now = datetime.utcnow()
    return db.query(DoctorSlot).filter(DoctorSlot.doctor_id == doctor_id, DoctorSlot.is_booked == False, DoctorSlot.start_datetime >= now).order_by(DoctorSlot.start_datetime).all()
