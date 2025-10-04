FROM python:3.12.3

RUN apt-get update && apt-get install -y \
    vim \
    curl

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry --break-system-packages && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY src /app/src
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh