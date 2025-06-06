import sys
import os
from gtts import gTTS
import tempfile
from fastapi.responses import FileResponse

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

from agents.common.audio_utils import clean_text_for_speech

def speak_summary(summary):
    try:
        summary_text = summary.get("summary", "") if isinstance(summary, dict) else summary
        if not summary_text or not isinstance(summary_text, str):
            raise ValueError("Summary must be a non-empty string.")

        cleaned_text = clean_text_for_speech(summary_text)
        tts = gTTS(text=cleaned_text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            return fp.name  # Return path to generated audio

    except Exception as e:
        print("Speech Error:", str(e))
        return None














# import re
# from gtts import gTTS
# import os
# import tempfile
# import platform

# if platform.system() == "Windows":
#     from playsound import playsound
# else:
#     import subprocess

    

# from agents.common.audio_utils import clean_text_for_speech

# def speak_summary(summary):
#     try:
#         if isinstance(summary, dict):
#             summary_text = summary.get("summary", "")
#         else:
#             summary_text = summary

#         if not summary_text or not isinstance(summary_text, str):
#             raise ValueError("Summary must be a non-empty string.")

#         cleaned_text = clean_text_for_speech(summary_text)
#         tts = gTTS(text=cleaned_text, lang='en')
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
#             tts.save(fp.name)
#             audio_path = fp.name

#         if platform.system() == "Windows":
#             playsound(audio_path)
#         else:
#             subprocess.call(["afplay", audio_path])

#         os.unlink(audio_path)

#     except Exception as e:
#         print("Speech Error:", str(e))
#         return {"error": str(e)}
