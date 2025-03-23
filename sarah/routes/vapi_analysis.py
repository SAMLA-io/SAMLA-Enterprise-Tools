from fastapi import FastAPI, HTTPException
import requests
import dotenv
import os

dotenv.load_dotenv()

app = FastAPI()

auth_token = os.getenv('VAPI_AUTH_TOKEN')
assistant_id = os.getenv('VAPI_ASSISTANT_ID')

headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json'
}

def get_latest_call_id():
    response = requests.get(
        'https://api.vapi.ai/call',
        headers=headers,
        params={'assistantId': assistant_id}
    )
    if response.status_code == 200:
        calls = response.json()
        if calls:
            return calls[0]['id']
        else:
            raise HTTPException(status_code=404, detail="No calls found for this assistant")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve calls list")

def get_call_data():
    call_id = get_latest_call_id()
    response = requests.get(f'https://api.vapi.ai/call/{call_id}', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve call data")

@app.get("/call_ids")
def get_all_call_ids():
    response = requests.get(
        'https://api.vapi.ai/call',
        headers=headers,
        params={'assistantId': assistant_id}
    )
    if response.status_code == 200:
        calls = response.json()
        if calls:
            call_ids = [call['id'] for call in calls]
            return {"Call IDs": call_ids}
        else:
            return {"message": "No calls found for this assistant"}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve call list")


@app.get("/basic_info")
def basic_info():
    call_data = get_call_data()
    print(call_data)
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
    try:
        call_data = get_call_data()
        customer_number = call_data.get('customer', {}).get('number', "Web")
    except Exception:
        customer_number = "Web"
    
    return {
        "Customer Number": customer_number
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("vapi_analysis:app", host="0.0.0.0", port=8000, reload=True)