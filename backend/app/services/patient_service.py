from pydantic import BaseModel
from typing import Optional, List

# --- Modeller ---

class PatientProfile(BaseModel):
    ad: str
    yas: int
    cinsiyet: str  # "erkek" | "kadın" | "belirtmek istemiyorum"
    kronik_hastaliklar: Optional[List[str]] = []
    kullanilan_ilaclar: Optional[List[str]] = []
    alerjiler: Optional[List[str]] = []

# Geçici bellek (Firebase eklenince burası değişecek)
patient_db: dict = {}

# --- Fonksiyonlar ---

def create_patient(patient_id: str, profile: PatientProfile) -> dict:
    patient_db[patient_id] = profile.model_dump()
    return {"message": "Hasta profili oluşturuldu", "patient_id": patient_id}

def get_patient(patient_id: str) -> Optional[dict]:
    return patient_db.get(patient_id)

def build_patient_context(patient_id: str) -> str:
    """Hasta bilgilerini GPT-4o'ya gönderilecek formata çevirir."""
    patient = get_patient(patient_id)
    if not patient:
        return ""
    
    return f"""
Hasta Bilgileri:
- Ad: {patient['ad']}, Yaş: {patient['yas']}, Cinsiyet: {patient['cinsiyet']}
- Kronik Hastalıklar: {', '.join(patient['kronik_hastaliklar']) or 'Yok'}
- Kullanılan İlaçlar: {', '.join(patient['kullanilan_ilaclar']) or 'Yok'}
- Alerjiler: {', '.join(patient['alerjiler']) or 'Yok'}
"""