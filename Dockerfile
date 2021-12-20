FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN python3 -m pip install --upgrade pip setuptools

RUN python3 -m pip install -r requirements.txt

CMD ["uvicorn", "--host", "0.0.0.0", "api.main:app"]
