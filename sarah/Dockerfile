FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    git

RUN pip install -r requirements.txt

EXPOSE 8002
CMD ["fastapi", "run", "routes/vapi_analysis.py", "--port", "8002"]
