import asyncio

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from ..services.transcription import (
    transcribe_audio,
)

from ..services.translation import (
    translate_to_english,
)


router = APIRouter(
    tags=["Transcription"],
)


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


                    # -------------------------
                    # 3. Send to React
                    # -------------------------

                    await websocket.send_json({

                        "type": "transcript",

                        "original_text":
                            original_text,

                        "language":
                            detected_language,

                        "english_text":
                            english_text,

                    })


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