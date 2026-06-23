FROM python:3.10-slim

WORKDIR /app

# Core build requirements
RUN apt-get update && apt-get install -y gcc librdkafka-dev pkg-config && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment port variable default (Docker-compose isey override kar lega)
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]