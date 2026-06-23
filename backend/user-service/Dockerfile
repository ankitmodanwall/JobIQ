FROM python:3.10-slim

WORKDIR /app

# Core build requirements
RUN apt-get update && apt-get install -y gcc librdkafka-dev pkg-config && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ✅ FIX: Port 8001 expose karo
EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]