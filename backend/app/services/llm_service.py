import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

from app.core.prompts import SYSTEM_PROMPT

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("JSON bulunamadı")
    return json.loads(match.group())


def call_llm(text: str, context: str = "") -> dict:

    rag_block = f"\nTıbbi Rehber:\n{context}" if context.strip() else "\nTıbbi Rehber: Yok"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT + rag_block
            },
            {
                "role": "user",
                "content": f"Hasta şikayeti: {text}"
            }
        ],
        temperature=0.2,
        max_tokens=500
    )

    raw = response.choices[0].message.content

    print("RAW:", raw)

    result = extract_json(raw)

    # ZORUNLU FIELD CHECK
    required = [
        "aciliyet",
        "aciliyet_emoji",
        "bolum",
        "aciklama",
        "uyari"
    ]

    for r in required:
        if r not in result:
            raise ValueError(f"Eksik field: {r}")

    return result