from cerebraai.models.orchestrator import Orchestrator
from cerebraai.models.llm import LLM, LLMConditions
from sentence_transformers import SentenceTransformer
from .models.agent import Agent

from openai import OpenAI
from dotenv import load_dotenv
import os

import nltk
nltk.download('punkt_tab')
nltk.download('vader_lexicon')

load_dotenv()

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

RAG_URL = os.getenv("RAG_URL")

MONGO_AWS_URL = os.getenv("MONGO_AWS_URL")
MONGO_AWS_TOKEN = os.getenv("MONGO_AWS_TOKEN")
MONGO_CHAT_HISTORY_COLLECTION = os.getenv("MONGO_CHAT_HISTORY_COLLECTION")

# SETUP: 
client = OpenAI(api_key=OPENAI_API_KEY)

def execute_openai_4(messages):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": messages
            }
        ]
    )  
    return response.choices[0].message.content

def execute_openai_4o(messages):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": messages
            }
        ]
    )
    return response.choices[0].message.content

def execute_openai_3_5(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": messages
            }
        ]
    )
    return response.choices[0].message.content

llms = [
    LLM("gpt-4", LLMConditions(domain="creativity", sentiment="positive", topic="arts", description="Optimized for reasoning, creativity, and complex tasks."), execute_openai_4),
    LLM("gpt-4o", LLMConditions(domain="general", sentiment="positive", topic="general", description="Moderately optimized for balanced tasks and cost-efficiency."), execute_openai_4o),
    LLM("gpt-3.5-turbo", LLMConditions(domain="general", sentiment="positive", topic="general", description="Suitable for simple, straightforward tasks."), execute_openai_3_5),
]

weights: dict = {"semantic": 0.3, "topic": 0.5, "sentiment": 0.3}
sentiment_weights: dict = {"positive": 0.5, "negative": 0.5}
emotion_weights: dict = {"happy": 0.5, "sad": 0.5}

orchestrator = Orchestrator(
    llms=llms,
    text_model=SentenceTransformer("all-MiniLM-L12-v2"),
    analysis_weights=weights,
    sentiment_weights=sentiment_weights,
    emotion_weights=emotion_weights
)

agent = Agent("SAMUEL", accepted_files=["pdf", "docx", "txt", "csv", "xlsx"], rag=True)

def execute_orchestrator(prompt: str, weights: dict = weights, sentiment_weights: dict = sentiment_weights, emotion_weights: dict = emotion_weights):
    return orchestrator.execute(prompt, weights, sentiment_weights, emotion_weights)

