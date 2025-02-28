# Written by Juan Pablo Gutiérrez

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent.helpers.session_manager import generate_session_id
from .routes.chat import router as chat_router
from .routes.graphs import router as graphs_router
from .routes.recommendations import router as recommendations_router
from .routes.audio import router as audio_router
from .setup import agent

import uvicorn

app = FastAPI()

app.include_router(chat_router)
app.include_router(graphs_router)
app.include_router(recommendations_router)
app.include_router(audio_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": f"Hello World, SAMLA {agent.name} is running"}

@app.get("/session")
def get_session():
    """
    This endpoint is used to generate a new session id.

    It is used to identify the session of the user. Must be used in the first request to the server.
    """

    return {"session_id": generate_session_id()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)