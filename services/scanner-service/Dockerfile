FROM python:3.11

ENV POETRY_VERSION=1.7.1
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY ../../pyproject.toml /app/pyproject.toml

RUN poetry config virtualenvs.create false     && poetry install --no-interaction --no-ansi

COPY ./app ./app

CMD ["python", "app/main.py"]
