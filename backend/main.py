from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.services.rag_service import get_medical_context
from app.services.llm_service import call_llm
from app.services.speech_service import transcribe_audio
from auth import hash_password, verify_password
from database import SessionLocal, engine, Base
from models import User

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = os.getenv("SECRET_KEY", "gizlikey123")
ALGORITHM = "HS256"
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(days=7)
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.id == payload["id"]).first()
        if not user:
            raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz token")

# MODELS
class TriageRequest(BaseModel):
    semptomlar: str
    duration: Optional[str] = None
    severity: Optional[str] = None

class LoginRequest(BaseModel):
    kullanici: str
    sifre: str
    rol: Optional[str] = "hasta"

class RegisterRequest(BaseModel):
    kullanici: str
    email: Optional[str] = None
    sifre: str
    rol: Optional[str] = "hasta"
    full_name: Optional[str] = None

class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    blood_type: Optional[str] = None
    chronic_diseases: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None

# ENDPOINTS
@app.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == req.kullanici).first()
    if existing:
        raise HTTPException(status_code=400, detail="Kullanıcı zaten var")
    user = User(
        username=req.kullanici,
        email=req.email,
        password_hash=hash_password(req.sifre),
        role="doctor" if req.rol == "doktor" else "patient",
        full_name=req.full_name or req.kullanici
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token({"id": user.id, "rol": user.role})
    return {"success": True, "token": token, "user": {"id": user.id, "kullanici": user.username, "rol": user.role}}

@app.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.kullanici).first()
    if not user or not verify_password(req.sifre, user.password_hash):
        raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")
    token = create_token({"id": user.id, "rol": user.role})
    return {"success": True, "token": token, "user": {"id": user.id, "kullanici": user.username, "rol": user.role}}

@app.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {"success": True, "data": {
        "id": current_user.id,
        "kullanici": current_user.username,
        "email": current_user.email,
        "rol": current_user.role,
        "age": current_user.age,
        "gender": current_user.gender,
        "height": current_user.height,
        "weight": current_user.weight,
        "blood": current_user.blood_type,
        "chronic": current_user.chronic_diseases,
        "allergies": current_user.allergies,
        "medications": current_user.medications,
    }}

@app.put("/profile")
def update_profile(req: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for key, value in req.dict(exclude_none=True).items():
        setattr(current_user, key, value)
    db.commit()
    return {"success": True}

@app.post("/triage")
async def triage_endpoint(request: TriageRequest):
    try:
        context = get_medical_context(request.semptomlar)
        result = call_llm(text=request.semptomlar, context=context)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe")
async def transcribe_endpoint(audio: UploadFile = File(...)):
    try:
        audio_bytes = await audio.read()
        text = transcribe_audio(audio_bytes)
        return {"success": True, "text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/medications")
def get_medications(current_user: User = Depends(get_current_user)):
    return {"success": True, "data": []}

@app.get("/triage/history")
def get_history(current_user: User = Depends(get_current_user)):
    return {"success": True, "data": []}

@app.get("/doctor/requests")
def get_doctor_requests(current_user: User = Depends(get_current_user)):
    return {"success": True, "data": []}

@app.put("/doctor/request/{id}")
def update_request(id: int, current_user: User = Depends(get_current_user)):
    return {"success": True}

@app.post("/prescription-request")
def prescription_request(current_user: User = Depends(get_current_user)):
    return {"success": True}