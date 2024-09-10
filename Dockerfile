FROM python:3.8.13-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt


COPY .env /app/.env


ENV PYTHONUNBUFFERED 1

EXPOSE 3008

CMD ["python", "api.py"]
