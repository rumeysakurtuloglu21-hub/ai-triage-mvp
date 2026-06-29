# 🏥 AI Triage Sistemi

Yapay zeka destekli akıllı sağlık ön değerlendirme sistemi.

## 🚀 Proje Hakkında

AI Triage, kullanıcıların semptomlarını analiz ederek:

- Risk seviyesini belirler (Düşük / Orta / Yüksek)
- Uygun sağlık bölümünü önerir
- Doktora yönlendirme sağlar
- Sesli semptom girişini destekler
- Hasta sağlık profilini yönetir
- Kronik ilaç yenileme talebi oluşturur

> ⚠️ Bu sistem tıbbi tanı koymaz. Sadece yapay zeka destekli ön değerlendirme sağlar.

## 🛠 Kullanılan Teknolojiler

**Frontend:**
- React
- Vite
- React Router
- JavaScript / CSS

**Backend:**
- FastAPI
- SQLAlchemy
- PyMySQL
- Groq (LLM)
- Python Jose (JWT)

**Veritabanı:**
- MySQL (Railway)

**Deploy:**
- Render (Frontend & Backend)

## 📂 Proje Yapısı

```
ai-triage-mvp/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── auth.py
│   ├── requirements.txt
│   └── app/
│       ├── services/
│       │   ├── llm_service.py
│       │   ├── speech_service.py
│       │   └── rag_service.py
│       └── core/
│           └── prompts.py
└── frontend/
    └── src/
        ├── pages/
        ├── components/
        ├── context/
        ├── styles/
        └── utils/
```

## ⚙️ Kurulum

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🔌 API Endpoint'leri

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | /register | Kayıt ol |
| POST | /login | Giriş yap |
| GET | /profile | Profil getir |
| PUT | /profile | Profil güncelle |
| POST | /triage | AI analiz |
| POST | /transcribe | Ses → Metin |
| GET | /medications | İlaçlar |
| GET | /triage/history | Geçmiş |

## 🌐 Canlı Demo

- **Frontend:** https://ai-triage-frontend.onrender.com
- **Backend:** https://ai-triage-mvp-1.onrender.com
- **API Docs:** https://ai-triage-mvp-1.onrender.com/docs

## 👥 Geliştiriciler

| Rol | İsim |
|-----|------|
| Frontend | Sudenas Baygın |
| Backend | Rümeysa Kültüroğlu |