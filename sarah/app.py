from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from routes import knowledge_base, people_directory, semantic_search, text_to_speech, speech_to_text, live_responses, json_storage, sentiment_analysis

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.include_router(knowledge_base.router, prefix="/knowledge_base")
app.include_router(people_directory.router, prefix="/people_directory")
app.include_router(semantic_search.router, prefix="/semantic_search")
app.include_router(text_to_speech.router, prefix="/text_to_speech")
app.include_router(speech_to_text.router, prefix="/speech_to_text")
app.include_router(live_responses.router, prefix="/live_responses")
app.include_router(json_storage.router, prefix="/json_storage")
app.include_router(sentiment_analysis.router, prefix="/sentiment_analysis")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
