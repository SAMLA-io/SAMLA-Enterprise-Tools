FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    git

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

EXPOSE 8002
CMD ["fastapi", "run", "routes/vapi_analysis.py", "--port", "8002"]
