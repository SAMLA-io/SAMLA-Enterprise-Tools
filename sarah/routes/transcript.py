import asyncio
import json
import os

from flask import Flask, request, render_template
from deepgram import Deepgram
from twilio.twiml.voice_response import Dial, VoiceResponse
from twilio.rest import Client
from pysondb import db
from dotenv import load_dotenv

app = Flask(__name__)

calls_db=db.getDb('calls')

load_dotenv()

@app.post("/inbound")
def inbound_call():
  response = VoiceResponse()
  dial = Dial(
      record='record-from-answer-dual',
      recording_status_callback='https://6d71-104-6-9-133.ngrok.io/recordings'
      )

  dial.number(os.getenv("RECEIVER_NUMBER"))
  response.append(dial)

  return str(response)

@app.route("/recordings", methods=['GET', 'POST'])
async def get_recordings():
   deepgram = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

   recording_url = request.form['RecordingUrl']
   source = {'url': recording_url}
   transcript_data = await deepgram.transcription.prerecorded(source, {'punctuate': True,
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
   
@app.route("/transcribe", methods=['GET', 'POST'])
def transcribe_call():
   context = calls_db.getAll()
   return render_template("index.html", context=context )


if __name__ == "__main__":
   app.run(debug=True)