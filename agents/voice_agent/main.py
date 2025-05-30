from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from ..agents.common.audio_utils import speak_summary
import os

app = FastAPI()

# Allow CORS for web browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Voice Agent is running!"}

@app.get("/speak/")
def speak(text: str = Query(..., description="Text to speak")):
    audio_path = speak_summary(text)
    if not audio_path or not os.path.exists(audio_path):
        return {"error": "Audio generation failed"}
    
    # Return audio file (auto-deletes after send)
    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        filename="summary.mp3"
    )











# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


# from fastapi import FastAPI, Query
# from agents.common.audio_utils import speak_summary


# app = FastAPI()

# @app.get("/")
# def root():
#     return {"message": "Voice Agent is running!"}

# @app.get("/speak/")
# def speak(text: str = Query(..., description="Text to speak")):
#     speak_summary(text)
#     return {"status": "Spoken"}
