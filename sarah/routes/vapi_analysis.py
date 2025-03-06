from fastapi import FastAPI, HTTPException
import requests
import dotenv
import os

dotenv.load_dotenv()

app = FastAPI()

auth_token = os.getenv('VAPI_AUTH_TOKEN')
call_id = '68611081-f21a-4da8-9643-5d81814ff334'

headers = {
    'Authorization': f'Bearer {auth_token}',
}

def get_call_data():
    response = requests.get(f'https://api.vapi.ai/call/{call_id}', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve call data")

@app.get("/basic_info")
def basic_info():
    call_data = get_call_data()
    return {
        "Call ID": call_data['id'],
        "Type": call_data['type'],
        "Started At": call_data['startedAt'],
        "Ended At": call_data['endedAt'],
        "Status": call_data['status'],
        "Ended Reason": call_data['endedReason']
        
    }

@app.get("/analysis")
def analysis():
    call_data = get_call_data()
    return {
        "Summary": call_data['analysis']['summary'],
        "Topics": call_data['analysis']['structuredData'],
        "Success Evaluation": call_data['analysis']['successEvaluation']
    }

@app.get("/customer_info")
def customer_info():
    call_data = get_call_data()
    return {
        "Customer Number": call_data['customer']['number']
    }

@app.get("/transcript")
def transcript():
    call_data = get_call_data()
    return {
        "Transcript": call_data['transcript']
    }

@app.get("/recording_urls")
def recording_urls():
    call_data = get_call_data()
    return {
        "Recording URL": call_data['recordingUrl'],
        "Stereo Recording URL": call_data['stereoRecordingUrl']
    }

@app.get("/cost_breakdown")
def cost_breakdown():
    call_data = get_call_data()
    return call_data['costBreakdown']