1. python3 -m venv venv
2. source venv/bin/activate
3. pip install fastapi uvicorn sqlalchemy psycopg2-binary "passlib[bcrypt]" "python-jose[cryptography]" python-dotenv alembic
4. mkdir auth users
5. touch auth/__init__.py auth/models.py auth/routes.py auth/security.py
6. touch users/__init__.py users/db.py users/models.py users/crud.py
7. touch main.py
8. alembic init alembic
9. # Generate a new migration
alembic revision --autogenerate -m "Add email and phone_number to users"
# OR
python -m alembic revision --autogenerate -m "added patient, doctor, appointments, infections"
10. # Apply migration to DB
alembic upgrade head
11. # To run
uvicorn main:app --reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000


# To check in postgresql : 
psql -U riddhi -d dermaai -h localhost -p 5432


# dermaai_backend
