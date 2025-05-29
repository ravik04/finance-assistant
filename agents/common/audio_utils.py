from gtts import gTTS
import os
import platform
import uuid

if platform.system() == "Windows":
    from playsound import playsound
else:
    import subprocess


import re

def clean_text_for_speech(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"\n\s*[\*\-]\s*", ". ", text)
    text = re.sub(r"\n+", ". ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def speak_summary(text):
    try:
        if not text or not isinstance(text, str):
            raise ValueError("Summary must be a non-empty string.")

        cleaned_text = clean_text_for_speech(text)

        temp_filename = os.path.join(os.environ['TEMP'], f"speech_{uuid.uuid4().hex}.mp3")
        tts = gTTS(text=cleaned_text, lang="en")
        tts.save(temp_filename)

        if platform.system() == "Windows":
            playsound(temp_filename)
        else:
            subprocess.call(["afplay", temp_filename])

        os.remove(temp_filename)

    except Exception as e:
        print("Speech Error:", str(e))
        return {"error": str(e)}
