import os
import json
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Requires OpenAI API access
PORT = int(os.getenv('PORT', 5050))

# System message to guide the assistant's behavior
SYSTEM_MESSAGE = (
    "You are a helpful AI assistant prepared to chat about "
    "anything the user is interested in. You provide clear and concise responses."
)

# Initialize FastAPI
app = FastAPI()

if not OPENAI_API_KEY:
    raise ValueError('Missing the OpenAI API key. Please set it in the .env file.')

@app.get("/", response_class=HTMLResponse)
async def index_page():
    return "<h1>AI Assistant Server is Running!</h1>"

@app.websocket("/chat")
async def chat_with_ai(websocket: WebSocket):
    """WebSocket endpoint for bidirectional communication with the AI assistant."""
    await websocket.accept()
    print("Client connected to /chat")

    # Connect to the OpenAI WebSocket
    async with websockets.connect(
        'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01',
        extra_headers={"Authorization": f"Bearer {OPENAI_API_KEY}"}
    ) as openai_ws:
        await send_session_update(openai_ws)

        async def receive_from_client():
            """Receive user messages and forward them to OpenAI."""
            try:
                async for message in websocket.iter_text():
                    user_input = json.loads(message)
                    print(f"User said: {user_input}")
                    await openai_ws.send(json.dumps({
                        "type": "input.text",
                        "text": user_input.get("text", "")
                    }))
            except Exception as e:
                print(f"Error receiving from client: {e}")
                await websocket.close()

        async def send_to_client():
            """Receive AI responses and forward them to the client."""
            try:
                async for message in openai_ws:
                    response = json.loads(message)
                    if response["type"] == "response.text":
                        await websocket.send_json({"response": response["text"]})
            except Exception as e:
                print(f"Error sending to client: {e}")
                await websocket.close()

        # Handle bidirectional communication
        await asyncio.gather(receive_from_client(), send_to_client())

async def send_session_update(openai_ws):
    """Send session configuration to OpenAI WebSocket."""
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "instructions": SYSTEM_MESSAGE,
            "modalities": ["text"],
            "temperature": 0.8,
        }
    }
    print('Sending session update:', session_update)
    await openai_ws.send(json.dumps(session_update))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)