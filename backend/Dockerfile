FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app
COPY wait_for_db.py /app/wait_for_db.py
COPY alembic.ini /app/alembic.ini
COPY migrations /app/migrations

EXPOSE 8000

CMD ["bash", "-lc", "python /app/wait_for_db.py && (alembic upgrade head || echo 'Alembic failed, starting API anyway') && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
