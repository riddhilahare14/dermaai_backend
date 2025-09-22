# Derma AI Backend API 🏥🔬

A FastAPI-based backend service for AI-powered dermatological diagnosis and telemedicine platform. This system provides secure authentication, patient management, AI-powered skin condition analysis, and real-time video consultations.

## 🌟 Features

### Core Functionality
- **JWT Authentication**: Secure role-based authentication (Patient/Doctor/Admin)
- **AI-Powered Diagnosis**: Integration for skin condition analysis with confidence scoring
- **Appointment Management**: Smart slot booking and scheduling system
- **Video Consultations**: Agora-powered real-time video calling
- **Image Processing**: Cloudinary integration for secure image storage
- **Medical Records**: Patient profile and infection history tracking

### Role-Based Access
- **Patients**: Profile management, AI diagnosis, appointment booking
- **Doctors**: Slot creation, appointment management, patient consultations
- **Admins**: User management and system oversight

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Image Storage**: Cloudinary CDN
- **Video Calling**: Agora.io RTC SDK
- **Environment**: Python-dotenv for configuration
- **Validation**: Pydantic schemas

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL database
- Cloudinary account
- Agora.io account
- Virtual environment (recommended)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd derma-ai-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   # Database
   DATABASE_URL=postgresql://username:password@localhost/derma_ai_db
   
   # JWT Configuration
   SECRET_KEY=your-super-secret-jwt-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   
   # Cloudinary Configuration
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   
   # Agora Configuration
   AGORA_APP_ID=your-agora-app-id
   AGORA_APP_CERTIFICATE=your-agora-certificate
   ```

5. **Database Setup**
   ```bash
   # Create database tables
   python -c "from modules.core.db import engine, Base; from modules.users.models import User; from modules.patients.models import Patient; from modules.doctors.models import Doctor, DoctorSlot; from modules.appointments.models import Appointment; from modules.infections.models import InfectionRecord; Base.metadata.create_all(bind=engine)"
   ```

6. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📁 Project Structure

```
derma-ai-backend/
├── modules/
│   ├── core/
│   │   ├── db.py                    # Database configuration
│   │   ├── cloudinary_utils.py     # Image upload utilities
│   │   └── agora_utils.py          # Video token generation
│   ├── auth/
│   │   ├── schemas.py              # Authentication schemas
│   │   ├── security.py             # JWT & password utilities
│   │   └── routes.py               # Auth endpoints
│   ├── users/
│   │   ├── models.py               # User database model
│   │   ├── schemas.py              # User validation schemas
│   │   ├── crud.py                 # User database operations
│   │   └── routes.py               # User management endpoints
│   ├── patients/
│   │   ├── models.py               # Patient profile model
│   │   ├── schemas.py              # Patient schemas
│   │   ├── crud.py                 # Patient operations
│   │   └── routes.py               # Patient endpoints
│   ├── doctors/
│   │   ├── models.py               # Doctor & slot models
│   │   ├── schemas.py              # Doctor schemas
│   │   ├── crud.py                 # Doctor operations
│   │   └── routes.py               # Doctor endpoints
│   ├── appointments/
│   │   ├── models.py               # Appointment model
│   │   ├── schemas.py              # Appointment schemas
│   │   ├── crud.py                 # Booking logic
│   │   └── routes.py               # Appointment endpoints
│   ├── infections/
│   │   ├── models.py               # Infection record model
│   │   ├── schemas.py              # Diagnosis schemas
│   │   ├── crud.py                 # Medical record operations
│   │   └── routes.py               # AI diagnosis endpoints
│   └── video/
│       └── routes.py               # Video token endpoints
├── main.py                         # FastAPI application entry
├── requirements.txt                # Python dependencies
└── .env                           # Environment variables
```

## 📚 API Endpoints

### Authentication (`/auth`)
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/profile` - Get current user profile

### User Management (`/users`)
- `GET /users/` - List all users (admin only)
- `GET /users/{username}` - Get specific user
- `GET /users/role/{role}` - Get users by role
- `PUT /users/{username}/role` - Update user role (admin)
- `PUT /users/{username}/password` - Update password
- `DELETE /users/{username}` - Delete user (admin)

### Patient Management (`/patients`)
- `GET /patients/me` - Get patient profile
- `POST /patients/me` - Update patient profile (with image upload)

### Doctor Management (`/doctors`)
- `POST /doctors/me` - Create/update doctor profile
- `POST /doctors/me/slots` - Create individual time slot
- `GET /doctors/me/slots` - List available slots
- `POST /doctors/me/slots-range` - Create multiple slots in date range

### AI Diagnosis (`/infections`)
- `POST /infections/diagnose` - Upload image for AI analysis
- `POST /infections/{record_id}/consult` - Request consultation for diagnosis

### Appointments (`/appointments`)
- `POST /appointments/request` - Book earliest available appointment
- `GET /appointments/{id}/token` - Get Agora video token for consultation

### Video Calling (`/video`)
- `GET /video/token` - Generate Agora RTC token

## 🔒 Security Features

### Authentication & Authorization
- JWT tokens with configurable expiration
- Bcrypt password hashing
- Role-based access control (RBAC)
- Protected endpoints with dependency injection

### Data Protection
- SQL injection prevention via SQLAlchemy ORM
- Input validation with Pydantic schemas
- Secure file uploads with Cloudinary
- Environment variable configuration

## 🧠 AI Integration

The system includes a placeholder AI diagnosis function that you can replace with your actual AI model:

```python
def call_ai_model_on_image_bytes(image_bytes: bytes):
    # Replace this with your actual AI model integration
    # Examples: TensorFlow, PyTorch, cloud AI services
    return {
        "diagnosis": "Possible fungal infection",
        "confidence": 0.86,
        "advice": "Apply anti-fungal cream..."
    }
```

### Recommended AI Services
- **Google Cloud Vision API**
- **AWS Rekognition Custom Labels**
- **Azure Custom Vision**
- **Custom TensorFlow/PyTorch models**

## 📱 Video Consultation Setup

The system uses Agora.io for real-time video consultations. You need to:

1. Create an Agora account at [agora.io](https://www.agora.io)
2. Get your App ID and Certificate
3. Add them to your `.env` file
4. Implement `agora_utils.py` with token generation:

```python
# modules/core/agora_utils.py
import os
from agora_token_builder import RtcTokenBuilder

def generate_agora_token(channel_name: str, uid: int) -> str:
    app_id = os.getenv("AGORA_APP_ID")
    app_certificate = os.getenv("AGORA_APP_CERTIFICATE")
    
    # Token expires in 24 hours
    expiration_time_in_seconds = 24 * 3600
    
    return RtcTokenBuilder.buildTokenWithUid(
        app_id, app_certificate, channel_name, uid, 
        1, expiration_time_in_seconds  # 1 = publisher role
    )
```

## 🗄️ Database Schema

### Key Relationships
- Users (1:1) → Patients/Doctors
- Doctors (1:N) → DoctorSlots
- Appointments → Patient, Doctor, DoctorSlot
- InfectionRecords → Patient
- All models include timestamps and cascade deletes

### Sample Database Models

```python
# Core user with role-based access
class User(Base):
    id: int (PK)
    username: str (unique)
    email: str (unique) 
    phone_number: str (optional)
    hashed_password: str
    role: str (patient/doctor/admin)

# Extended patient profile
class Patient(Base):
    id: int (PK)
    user_id: int (FK → users.id)
    dob: date (optional)
    gender: str (optional)
    medical_history: JSON (optional)
    profile_image: str (optional)

# Doctor availability management
class DoctorSlot(Base):
    id: int (PK)
    doctor_id: int (FK → doctors.id)
    start_datetime: datetime
    end_datetime: datetime
    is_booked: boolean
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup for Production
```bash
# Use strong secrets in production
SECRET_KEY=$(openssl rand -hex 32)

# Use production database URL
DATABASE_URL=postgresql://user:pass@prod-db:5432/derma_ai

# Configure CORS for your frontend domain
CORS_ORIGINS=https://your-frontend-domain.com
```

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=modules tests/
```

## 📊 Performance Considerations

### Database Optimization
- Use connection pooling for high concurrency
- Add database indexes for frequently queried fields
- Implement caching for repeated queries

### Image Processing
- Compress images before AI processing
- Use async processing for large files
- Implement image size limits

### Video Calling
- Monitor Agora usage and costs
- Implement call duration limits
- Cache tokens when possible

## 🐛 Troubleshooting

### Common Issues

**Database Connection Errors**
```bash
# Check database is running
sudo systemctl status postgresql

# Verify connection string
echo $DATABASE_URL
```

**Cloudinary Upload Failures**
- Verify API credentials in `.env`
- Check file size limits
- Ensure stable internet connection

**JWT Token Issues**
- Check SECRET_KEY configuration
- Verify token expiration settings
- Ensure system clock synchronization

**Video Call Problems**
- Validate Agora App ID and Certificate
- Check token generation logic
- Verify network connectivity

## 🔮 Future Enhancements

- [ ] **Real AI Model Integration** - Replace placeholder with actual ML model
- [ ] **Push Notifications** - Appointment reminders and updates
- [ ] **Medical History Analytics** - Patient health trends
- [ ] **Multi-language Support** - Internationalization
- [ ] **Audit Logging** - Complete action history
- [ ] **Advanced Scheduling** - Recurring appointments, waitlists
- [ ] **Telemedicine Features** - Digital prescriptions, follow-ups
- [ ] **Performance Monitoring** - Application metrics and alerts

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**Built with 💊 and FastAPI for better healthcare accessibility**
