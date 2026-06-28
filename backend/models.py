from sqlalchemy import Column, Integer, String, Float, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True)
    password_hash = Column(String(255))
    role = Column(Enum('patient', 'doctor'), default='patient')
    full_name = Column(String(150), nullable=False)
    age = Column(Integer)
    gender = Column(Enum('male', 'female', 'other'))
    height = Column(Float)
    weight = Column(Float)
    blood_type = Column(String(10))
    chronic_diseases = Column(Text)
    allergies = Column(Text)
    medications = Column(Text)
    selected_doctor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())