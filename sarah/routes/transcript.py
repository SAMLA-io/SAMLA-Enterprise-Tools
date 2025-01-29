import asyncio
import json
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from deepgram import Deepgram
from twilio.twiml.voice_response import Dial, VoiceResponse
from twilio.rest import Client
from pysondb import db
from dotenv import load_dotenv

app = FastAPI()

calls_db = db.getDb('calls')

load_dotenv()

@app.post("/inbound")
async def inbound_call():
    response = VoiceResponse()
    dial = Dial(
        record='record-from-answer-dual',
        recording_status_callback='https://6d71-104-6-9-133.ngrok.io/recordings'
    )

    dial.number(os.getenv("RECEIVER_NUMBER"))
    response.append(dial)

    return str(response)

@app.post("/recordings")
async def get_recordings(request: Request):
    deepgram = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

    form = await request.form()
    recording_url = form['RecordingUrl']
    source = {'url': recording_url}
    transcript_data = await deepgram.transcription.prerecorded(source, {
        'punctuate': True,
        'utterances': True,
        'model': 'phonecall',
        'multichannel': True
    })

    if 'results' in transcript_data:
        utterances = [
            {
                'channel': utterance['channel'],
                'transcript': utterance['transcript']
            } for utterance in transcript_data['results']['utterances']
        ]

        calls_db.addMany(utterances)

        return JSONResponse(content=utterances)

@app.get("/transcribe")
async def transcribe_call():
    context = calls_db.getAll()
    print(context)
    return JSONResponse(content=context)