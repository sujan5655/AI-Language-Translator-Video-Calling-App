from fastapi import FastAPI
import os 
import io
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from .auth.route import router as auth_router
from .auth.test_route import router as user_router
from .routes.transcription import (
    router as transcription_router,
)
#  Load Environment Variables
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
  raise RuntimeError("GROQ API Key is missing in .env")


# Fast API 
app=FastAPI()


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(transcription_router)


#Cors
app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174"
  ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)


# Groq

groq_client=Groq(
  api_key=GROQ_API_KEY
)




# Test Endpoint
@app.get("/")
async def root():
  return {
    "message":"AI Video Call Backend Running"
  }

# Transcription Feature
# def transcribe_audio(
#     audio_bytes:bytes,
#     language:str|None=None
# ):
#   audio_file=io.BytesIO(audio_bytes)
#   # Tell Groq what type of audio this is
#   audio_file.name = "audio.webm"
 
#   request={
#     "file":audio_file,
#     "model":"whisper-large-v3-turbo",
#     "response_format":"json",
#     "temperature":0.0,
#     "prompt":(
#       "This is a natural conversion"
#       "during a video call."
#       "Transcribe the speech accurately."
#       "Preserve names,technical terms,"
#       "add numbers."
#     )
#   }
  
#   result=groq_client.audio.transcriptions.create(
#     **request
#   )
#   detected_language=getattr(
#     result,"language",None
#   )
#   return {
#     "text":result.text.strip(),
#     "language":detected_language
#   }



