import io
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


def transcribe_audio(
    audio_bytes: bytes,
):
    audio_file = io.BytesIO(audio_bytes)

    # Tell Groq what type of audio file this is
    audio_file.name = "audio.webm"

    result = (
        groq_client
        .audio
        .transcriptions
        .create(
            file=audio_file,
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
            temperature=0.0,
            prompt=(
                "This is a natural conversation "
                "during a video call. "
                "Transcribe the speech accurately. "
                "Preserve names, technical terms, "
                "numbers, and important words."
            ),
        )
    )

    return {
        "text": result.text.strip(),
        "language": getattr(
            result,
            "language",
            None,
        ),
    }