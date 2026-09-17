import asyncio
import os 
from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)
from jose import JWTError,jwt
from ..models import User
from ..database import SessionLocal
from ..services.transcription import (
    transcribe_audio,
)

from ..services.translation import (
    translate_to_english,
)

from ..services.tts import generate_english_speech

router = APIRouter(
    tags=["Transcription"],
)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def authenticate_websocket(token: str):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        if payload.get("type") != "access":
            return None

        user_id = payload.get("sub")

        if user_id is None:
            return None

        db = SessionLocal()

        try:
            user = (
                db.query(User)
                .filter(User.id == int(user_id))
                .first()
            )

            return user

        finally:
            db.close()

    except (JWTError, ValueError, TypeError):
        return None

@router.websocket("/ws/transcription")
async def transcription_socket(
    websocket: WebSocket,
):

    await websocket.accept()

    print(
        "🟢 Transcription client connected"
    )

    try:

        while True:

            message = await websocket.receive()

            # Text messages
            if "text" in message:

                text = message["text"]

                if not text:
                    continue

                print(
                    f"📩 Text message: {text}"
                )

                continue


            # Audio messages
            if "bytes" in message:

                audio_bytes = message["bytes"]

                if not audio_bytes:
                    continue

                print(
                    f"🎧 Received "
                    f"{len(audio_bytes)} bytes"
                )

                try:

                    # -------------------------
                    # 1. Speech → Text
                    # -------------------------

                    transcription = (
                        await asyncio.to_thread(
                            transcribe_audio,
                            audio_bytes,
                        )
                    )

                    original_text = (
                        transcription["text"]
                    )

                    detected_language = (
                        transcription["language"]
                    )


                    if not original_text:
                        continue


                    print(
                        f"📝 Original: "
                        f"{original_text}"
                    )

                    print(
                        f"🌐 Language: "
                        f"{detected_language}"
                    )


                    # -------------------------
                    # 2. Text → English
                    # -------------------------

                    english_text = (
                        await asyncio.to_thread(
                            translate_to_english,
                            original_text,
                            detected_language,
                        )
                    )

                    print(
    f"🇬🇧 English: "
    f"{english_text}"
)


                    english_audio = await asyncio.to_thread(
    generate_english_speech,
    english_text,
)


                    print(
    f"🔊 English audio generated: "
    f"{len(english_audio)} bytes"
)


                    await websocket.send_json({
    "type": "transcript",
    "user_id": current_user.id,
    "username": current_user.username,
    "original_text": original_text,
    "language": detected_language,
    "english_text": english_text,
})


                    await websocket.send_bytes(
    english_audio
)


                except Exception as error:

                    print(
                        "❌ Processing error:",
                        error,
                    )

                    await websocket.send_json({

                        "type": "error",

                        "message":
                            str(error),

                    })


    except WebSocketDisconnect:

        print(
            "🔴 Transcription client disconnected"
        )

    except Exception as error:

        print(
            "❌ WebSocket error:",
            error,
        )