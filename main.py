# main.py
from fastapi import FastAPI
from modules.core.db import engine, Base
from modules.auth import routes as auth_routes
from modules.users import routes as user_routes
from modules.patients import routes as patient_routes
from modules.doctors import routes as doctor_routes
from modules.appointments import routes as appointment_routes
from modules.infections import routes as infection_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DermaAI Backend")

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(patient_routes.router)
app.include_router(doctor_routes.router)
app.include_router(appointment_routes.router)
app.include_router(infection_routes.router)
