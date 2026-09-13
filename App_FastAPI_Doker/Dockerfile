# Run: docker build -t app-fastapi . && docker run -d -p 8000:8000 --name app-fastapi-container app-fastapi

FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]