from aiohttp import web
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from deepgram import Deepgram
import os

# /inbound
async def inbound_handler(request):
    twiml = VoiceResponse()
    dial = twiml.dial(record="record-from-answer-dual", recording_status_callback="/transcribe")
    dial.number(os.getenv("FORWARDING_NUMBER"))
    return web.Response(text=str(twiml), content_type='text/xml')

# /transcribe
async def transcribe_handler(request):
    data = await request.post()
    recording_url = data.get('RecordingUrl')
    call_sid = data.get('CallSid')

    twilio_client = Client()
    call = twilio_client.calls(call_sid).fetch()
    caller = call.from_
    twilio_number = call.to

    options = {
        "punctuate": True,
        "tier": "enhanced",
        "summarize": True
    }

    deepgram_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))
    response = await deepgram_client.transcription.pre_recorded_url(
        {
            "url": recording_url
        },
        options
    )

    result = response.get("result")
    error = response.get("error")

    if error:
        raise Exception(error)

    summaries = result['results']['channels'][0]['alternatives'][0]['summaries']
    summary = "\n\n".join([s['summary'] for s in summaries])

    for number in [os.getenv("FORWARDING_NUMBER"), caller]:
        twilio_client.messages.create(
            body=summary,
            to=number,
            from_=twilio_number
        )

    return web.Response(text="true")

app = web.Application()
app.router.add_post('/inbound', inbound_handler)
app.router.add_post('/transcribe', transcribe_handler)

if __name__ == '__main__':
    web.run_app(app)