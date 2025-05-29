import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from fastapi import FastAPI, Query
from agents.common.audio_utils import speak_summary


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Voice Agent is running!"}

@app.get("/speak/")
def speak(text: str = Query(..., description="Text to speak")):
    speak_summary(text)
    return {"status": "Spoken"}
