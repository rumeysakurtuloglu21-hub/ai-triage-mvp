# 🏥 AI Triage System

An AI-powered intelligent medical pre-assessment system.

## 🚀 About the Project

AI Triage analyzes user symptoms to:

- Determine risk level (Low / Medium / High)
- Recommend the appropriate medical department
- Guide users to the right doctor
- Support voice symptom input
- Manage patient health profiles
- Create chronic medication renewal requests

> ⚠️ This system does not provide medical diagnosis. It only provides AI-assisted pre-assessment.

## 🛠 Technologies Used

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

**Database:**
- MySQL (Railway)

**Deployment:**
- Render (Frontend & Backend)

## 📂 Project Structure

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

## ⚙️ Installation

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

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /register | Register |
| POST | /login | Login |
| GET | /profile | Get profile |
| PUT | /profile | Update profile |
| POST | /triage | AI analysis |
| POST | /transcribe | Audio → Text |
| GET | /medications | Medications |
| GET | /triage/history | History |

## 🌐 Live Demo

- **Frontend:** https://ai-triage-frontend.onrender.com
- **Backend:** https://ai-triage-mvp-1.onrender.com
- **API Docs:** https://ai-triage-mvp-1.onrender.com/docs

## 👥 Developers

| Role | Name |
|------|------|
| Frontend | Sudenas Baygın |
| Backend | Rümeysa Kültüroğlu |
