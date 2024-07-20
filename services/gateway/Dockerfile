FROM python:3.12-alpine

RUN apk update && \
  apk add --no-cache \
    gcc \
    python3-dev \
    libressl-dev \
    musl-dev \
    libffi-dev \
    netcat-openbsd \
    bash

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry

WORKDIR /api

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install --no-root

COPY . .

COPY ./start.sh /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

CMD [ "/start" ]
