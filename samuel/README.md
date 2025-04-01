# SAMUEL

SAMUEL is an intelligent agent system that orchestrates multiple LLM models and includes RAG (Retrieval-Augmented Generation) capabilities.

## Features

- 🤖 Multi-model orchestration with GPT-4, GPT-4 Optimized, and GPT-3.5 Turbo
- 📚 RAG (Retrieval-Augmented Generation) support
- 📄 Multiple file format support (PDF, DOCX, TXT, CSV, XLSX)
- 🎤 Audio transcription support
- 📊 Graph generation capabilities
- 🔄 Intelligent model selection based on task requirements
- 💡 Sentiment and domain-aware processing
- 💬 Chat history and recommendations

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
MONGO_AWS_URL=your_mongo_url
MONGO_AWS_TOKEN=your_mongo_token
MONGO_CHAT_HISTORY_COLLECTION=your_collection_name
```

## Quick Start

1. Start the FastAPI server:
```bash
python agent/app.py
```

2. The server will start on `http://localhost:8000`

## API Endpoints

### Session Management
- `GET /session` - Generate a new session ID for tracking conversations

### Chat Endpoints
- `GET /input` - Send a text message to the agent
  - Parameters:
    - `organization_id`: Your organization ID
    - `session_id`: Session ID from `/session` endpoint
    - `user_id`: User identifier
    - `message`: Your message to the agent

- `POST /upload` - Upload a file for processing
  - Parameters:
    - `organization_id`: Your organization ID
    - `session_id`: Session ID from `/session` endpoint
    - `user_id`: User identifier
    - `message`: Context or question about the file
    - `file`: File to process (PDF, DOCX, TXT, CSV, XLSX)

### Audio Processing
- `POST /audio` - Process audio files
  - Parameters:
    - `organization_id`: Your organization ID
    - `session_id`: Session ID from `/session` endpoint
    - `user_id`: User identifier
    - `file`: Audio file to transcribe and process

### Graph Generation
- `GET /get_graphs` - Generate graphs from data
  - Parameters:
    - `x`: Comma-separated x-axis values
    - `y`: Comma-separated y-axis values

### Recommendations
- `GET /get_chat_recommendations` - Get chat recommendations based on history
  - Parameters:
    - `organization_id`: Your organization ID
    - `user_id`: User identifier
    - `session_id`: Session ID from `/session` endpoint

## Example Usage

1. Start a new session:
```bash
curl http://localhost:8000/session
```

2. Send a message:
```bash
curl "http://localhost:8000/input?organization_id=org123&session_id=session456&user_id=user789&message=Hello%20SAMUEL"
```

3. Upload a file:
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "organization_id=org123" \
  -F "session_id=session456" \
  -F "user_id=user789" \
  -F "message=Please analyze this document" \
  -F "file=@document.pdf"
```

4. Process audio:
```bash
curl -X POST "http://localhost:8000/audio" \
  -H "Content-Type: multipart/form-data" \
  -F "organization_id=org123" \
  -F "session_id=session456" \
  -F "user_id=user789" \
  -F "file=@audio.mp3"
```

## Response Format

All endpoints return JSON responses with the following structure:
```json
{
    "message": "Response content",
    "response_time": "Time taken to generate response",
    "context_time": "Time taken to fetch context",
    "chat_history_time": "Time taken to fetch chat history",
    "insert_history_time": "Time taken to insert into history"
}
```

## License

This project is open-sourced under the MIT License - see the LICENSE file for details.

## Contributing

- [@jpgtzg](https://github.com/jpgtzg)
