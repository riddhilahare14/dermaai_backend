# # modules/appointments/routes.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from modules.core.db import get_db
# from modules.auth.security import get_current_user
# from modules.users.models import User
# from modules.appointments import schemas, crud as appt_crud
# from modules.patients import crud as patient_crud
# from modules.core import agora_utils

# router = APIRouter(prefix="/appointments", tags=["appointments"])

# @router.post("/request", response_model=schemas.AppointmentOut)
# def request_appointment(payload: schemas.AppointmentRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     if current_user.role != "patient":
#         raise HTTPException(status_code=403, detail="Only patients can request appointments")
#     patient = patient_crud.get_patient_by_user_id(db, current_user.id)
#     if not patient:
#         raise HTTPException(status_code=404, detail="Patient profile not found")
#     appt = appt_crud.book_earliest_slot_across_doctors(db, patient.id, preferred_specialization=payload.preferred_specialization)
#     if not appt:
#         raise HTTPException(status_code=404, detail="No available slots found")
#     return appt

# @router.get("/{appointment_id}/token")
# def get_agora_token(appointment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
#     if not appt:
#         raise HTTPException(status_code=404, detail="Appointment not found")
    
#     # Only patient or doctor of this appointment
#     if appt.patient.user_id != current_user.id and appt.doctor.user_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not authorized")

#     uid = current_user.id
#     token = agora_utils.generate_agora_token(appt.channel_name, uid)

#     return {"channel_name": appt.channel_name, "token": token, "uid": uid}



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.core.db import get_db
from modules.auth.security import get_current_user
from modules.users.models import User
from modules.appointments.models import Appointment
from modules.appointments import schemas, crud as appt_crud
from modules.patients import crud as patient_crud

router = APIRouter(prefix="/appointments", tags=["appointments"])

# ---------------- Book Appointment ----------------
@router.post("/request", response_model=schemas.AppointmentOut)
def request_appointment(
    payload: schemas.AppointmentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can request appointments")

    patient = patient_crud.get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")

    appt = appt_crud.book_earliest_slot_across_doctors(
        db,
        patient.id,
        preferred_specialization=payload.preferred_specialization
    )

    if not appt:
        raise HTTPException(status_code=404, detail="No available slots found")
    return appt

# ---------------- Get Agora Token ----------------
@router.get("/{appointment_id}/token")
def get_agora_token(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appt.patient.user_id != current_user.id and appt.doctor.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    uid = current_user.id
    token = agora_utils.generate_agora_token(appt.channel_name, uid)
    return {"channel_name": appt.channel_name, "token": token, "uid": uid}


# ---------------- Get Upcoming Appointments for Patient ----------------
@router.get("/patient", response_model=list[schemas.AppointmentOut])
def get_patient_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can access this")

    patient = patient_crud.get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")

    return appt_crud.get_patient_upcoming_appointments(db, patient.id)


# ---------------- Get Upcoming Appointments for Doctor ----------------
@router.get("/doctor", response_model=list[schemas.AppointmentOut])
def get_doctor_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can access this")

    return appt_crud.get_doctor_upcoming_appointments(db, current_user.doctor_profile.id)
