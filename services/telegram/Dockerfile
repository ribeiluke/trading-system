FROM python:3.11-slim

ENV POETRY_VERSION=1.7.1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

ENV PYTHONPATH=/app

# system deps (some libs require compilation)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# upgrade pip FIRST
RUN python -m pip install --upgrade pip setuptools wheel

# install poetry
RUN pip install "poetry==$POETRY_VERSION"

# copy dependency files first (better cache)
COPY pyproject.toml poetry.lock ./

# install deps
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./services/telegram/app ./app
COPY ./shared ./shared

CMD ["python", "app/bot.py"]

