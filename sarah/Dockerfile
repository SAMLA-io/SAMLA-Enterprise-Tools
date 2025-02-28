FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    git

RUN pip install -r requirements.txt
    
CMD ["python", "app.py"]
