# Written by Juan Pablo Gutiérrez
# 27 01 2025

from fastapi import UploadFile
from openai import OpenAI
from ..setup import OPENAI_API_KEY
from ..helpers.prompting import ask

async def get_audio_processing(company_id: str, session_id: str, user_id: str, audio: UploadFile):
    """ 
    This function is used to process the audio into text.
    """
    
    audio_text = transcribe_audio(audio)

    response = await ask(company_id=company_id, user_id=user_id, session_id=session_id, prompt=audio_text, rag=True, insert_history=False)

    return response

def transcribe_audio(audio: UploadFile) -> str:
    """
    Transcribe the audio content using Whisper API.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    audio.file.seek(0)

    # Read the file content as bytes
    file_bytes = audio.file.read()

    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.mp3", file_bytes, "audio/mpeg"), 
    )

    return response.text