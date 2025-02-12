# SAMUEL

SAMUEL is an intelligent agent system that orchestrates multiple LLM models and includes RAG (Retrieval-Augmented Generation) capabilities.

## Features

- 🤖 Multi-model orchestration with GPT-4, GPT-4 Optimized, and GPT-3.5 Turbo
- 📚 RAG (Retrieval-Augmented Generation) support
- 📄 Multiple file format support (PDF, DOCX, TXT, CSV, XLSX)
- 🔄 Intelligent model selection based on task requirements
- 💡 Sentiment and domain-aware processing

## Installation

```bash
git clone https://github.com/samla-io/samla-enterprise-tools.git
cd samla-enterprise-tools
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in your project root with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
RAG_URL=your_rag_service_url
RAG_COLLECTION=your_rag_collection_name
MONGO_AWS_URL=your_mongo_url
MONGO_AWS_TOKEN=your_mongo_token
MONGO_CHAT_HISTORY_COLLECTION=your_collection_name
```

## Quick Start

All setup is done in the `setup.py` file.

1. Initialize dotenv variables
2. Create the LLMs and start the orchestrator. You can add more LLMs to the orchestrator if you want, as long as they have the same structure as the ones already there (the executor returns a valid response).
3. You can also change the weights of the orchestrator to give more or less importance to each LLM.
4. The necessary weights are:
    - weight between the importance of the semantic, topic and sentiment.
    - weight between the importance of the positive and negative sentiments.
    - weight between the importance of the happy and sad and other emotions.
5. These weights can be overridden in the `execute_orchestrator` function.

```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

RAG_URL = os.getenv("RAG_URL")
RAG_COLLECTION = os.getenv("RAG_COLLECTION")

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
    weights=weights,
    sentiment_weights=sentiment_weights,
    emotion_weights=emotion_weights
)
```

3. Create the agent and start the chat

```python
agent = Agent("SAMUEl", accepted_files=["pdf", "docx", "txt", "csv", "xlsx"], rag=True)
```

4. Run `fastapi run agent/app.py --port 8000` to start the FastAPI server

## License

This project is open-sourced under the MIT License - see the LICENSE file for details.

## Contributing

- [@jpgtzg](https://github.com/jpgtzg)
