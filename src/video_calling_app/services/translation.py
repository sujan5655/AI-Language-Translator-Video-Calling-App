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


def translate_to_english(
    text: str,
    source_language: str | None = None,
) -> str:

    if not text.strip():
        return ""

    language_info = ""

    if source_language:
        language_info = (
            f"The detected source language is "
            f"{source_language}."
        )

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a real-time translation "
                    "assistant for a video call. "
                    "Translate the user's speech into "
                    "natural English. "
                    "Preserve the original meaning, "
                    "names, numbers, technical terms, "
                    "and important details. "
                    "Do not explain the translation. "
                    "Return only the English translation."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"{language_info}\n\n"
                    f"Text:\n{text}"
                ),
            },
        ],
    )

    return response.choices[0].message.content.strip()