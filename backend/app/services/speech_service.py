import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(audio_file) -> str:
    """Ses dosyasını metne çevirir (Whisper)."""
    try:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=("audio.ogg", audio_file, "audio/ogg"),
            language="tr"
        )
        return transcription.text
    except Exception as e:
        raise RuntimeError(f"Ses tanıma hatası: {str(e)}")