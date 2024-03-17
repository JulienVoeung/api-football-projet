FROM python:3.11.7-slim-bullseye

COPY update-database.py /app/app.py
COPY s3.py /app/s3.py
COPY requirements.txt /app/requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "/app/app.py"]

