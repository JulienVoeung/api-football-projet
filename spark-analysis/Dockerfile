FROM python:3.11.7-slim-bullseye

COPY analyse.py /app/script.py
COPY database.py /app/database.py

COPY requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir -r /app/requirements.txt


CMD ["python", "/app/script.py"]