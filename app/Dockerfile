FROM python:3.12-alpine

WORKDIR /app

COPY ../requirements.txt .
COPY ../.env .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "app.main"]

