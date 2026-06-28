from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.services.rag_service import get_medical_context
from app.services.llm_service import call_llm

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# REQUEST MODEL
class TriageRequest(BaseModel):
    semptomlar: str
    duration: Optional[str] = None
    severity: Optional[str] = None


# RESPONSE ENDPOINT
@app.post("/triage")
async def triage_endpoint(request: TriageRequest):

    try:
        context = get_medical_context(request.semptomlar)

        result = call_llm(
            text=request.semptomlar,
            context=context
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))