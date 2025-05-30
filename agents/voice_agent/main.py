import sys
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)


from agents.common.audio_utils import speak_summary

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
    # Try to generate and return audio (if implemented)
    audio_path = speak_summary(text)
    if audio_path:
        # If you have audio file generation, return the file as well
        from fastapi.responses import FileResponse
        return FileResponse(audio_path, media_type="audio/mpeg", filename="summary.mp3")
    # Always return the text that was spoken
    return {"spoken_text": text}



# @app.get("/speak/")
# def speak(text: str = Query(..., description="Text to speak")):
#     audio_path = speak_summary(text)
#     if not audio_path or not os.path.exists(audio_path):
#         return {"error": "Audio generation failed"}
    
#     # Return audio file (auto-deletes after send)
#     return FileResponse(
#         audio_path,
#         media_type="audio/mpeg",
#         filename="summary.mp3"
    # )


















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
