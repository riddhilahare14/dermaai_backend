# modules/appointments/crud.py
from sqlalchemy.orm import Session
from modules.doctors.models import Doctor, DoctorSlot
from modules.appointments.models import Appointment
from modules.doctors import crud as doctor_crud
from modules.core import agora_utils
from datetime import datetime
import uuid

def book_earliest_slot_across_doctors(db: Session, patient_id: int, preferred_specialization: str | None = None):
    """
    Booking algorithm:
    - get doctors (optionally filtered by specialization) ordered by ID (sequential).
    - for each doctor: find the earliest unbooked slot (start >= now).
    - reserve the first found slot by setting is_booked True and creating an Appointment.
    NOTE: This is a simple approach. For concurrency use DB-level locks or SELECT ... FOR UPDATE.
    """
    now = datetime.utcnow()
    query = db.query(Doctor)
    if preferred_specialization:
        query = query.filter(Doctor.specialization == preferred_specialization)
    doctors = query.order_by(Doctor.id).all()

    for doc in doctors:
        # find earliest unbooked slot for this doctor
        slot = (
            db.query(DoctorSlot)
            .filter(DoctorSlot.doctor_id == doc.id, DoctorSlot.is_booked == False, DoctorSlot.start_datetime >= now)
            .order_by(DoctorSlot.start_datetime)
            .with_for_update()  # try to lock row where supported
            .first()
        )
        if slot:
            slot.is_booked = True
            # generate Agora channel
            channel_name = f"appt_{uuid.uuid4().hex[:8]}"
            patient_token = agora_utils.generate_agora_token(channel_name, patient_id)
            doctor_token = agora_utils.generate_agora_token(channel_name, doc.id)

            appt = Appointment(
                patient_id=patient_id,
                doctor_id=doc.id,
                slot_id=slot.id,
                scheduled_at=slot.start_datetime,
                status="scheduled",
                channel_name=channel_name,
                agora_token=patient_token  # store one token or generate fresh on request
            )
            db.add(appt)
            db.commit()
            db.refresh(appt)
            return appt
    return None

# ---------------- Upcoming Appointments ----------------

def get_patient_upcoming_appointments(db: Session, patient_id: int):
    """Return upcoming appointments for patient sorted by scheduled_at."""
    now = datetime.utcnow()
    return (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient_id)
        .filter(Appointment.scheduled_at >= now)
        .order_by(Appointment.scheduled_at.asc())
        .all()
    )

def get_doctor_upcoming_appointments(db: Session, doctor_id: int):
    """Return upcoming appointments for doctor sorted by scheduled_at."""
    now = datetime.utcnow()
    return (
        db.query(Appointment)
        .filter(Appointment.doctor_id == doctor_id)
        .filter(Appointment.scheduled_at >= now)
        .order_by(Appointment.scheduled_at.asc())
        .all()
    )
