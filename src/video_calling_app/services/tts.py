import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing in .env"
    )

groq_client = Groq(
    api_key=GROQ_API_KEY
)


TTS_MODEL = "canopylabs/orpheus-v1-english"

TTS_VOICE = "autumn"


def generate_english_speech(
    text: str,
) -> bytes:

    text = text.strip()

    if not text:
        return b""

    # Orpheus currently accepts up to 200 characters.
    if len(text) > 200:
        text = text[:200]

    response = groq_client.audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=text,
        response_format="wav",
    )

    return response.read()