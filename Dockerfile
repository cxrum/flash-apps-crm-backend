FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./alembic ./alembic
COPY ./app ./app
COPY ./etc ./etc
COPY ./tests ./tests
COPY ./alembic.ini ./alembic.ini
COPY ./pytest.ini ./pytest.ini 

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host ${API_HOST} --port ${API_PORT}"]
