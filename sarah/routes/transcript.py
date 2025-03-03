import os
import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from deepgram import Deepgram
from twilio.twiml.voice_response import Dial, VoiceResponse
from pysondb import db
from dotenv import load_dotenv

app = FastAPI()
templates = Jinja2Templates(directory="templates")

calls_db = db.getDb('calls')

load_dotenv()

@app.post("/inbound")
async def inbound_call():
    response = VoiceResponse()
    dial = Dial(
        record='record-from-answer-dual',
        recording_status_callback='https://1fd4-189-175-57-181.ngrok-free.app/recordings'
    )
    dial.number(os.getenv("RECEIVER_NUMBER"))
    response.append(dial)
    return HTMLResponse(content=str(response), status_code=200)

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

        return json.dumps(utterances, indent=4)

@app.get("/transcribe", response_class=HTMLResponse)
async def transcribe_call(request: Request):
    context = calls_db.getAll()
    return templates.TemplateResponse("template.html", {"request": request, "context": context})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)