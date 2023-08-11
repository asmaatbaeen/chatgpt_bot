# docker build -t slackgpt_bot .
# docker run slackgpt_bot
FROM python:3.9.6-slim as builder

ENV POETRY_VERSION=1.4.2

# Install dependencies required for installing packages
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt-get -qq install -y curl build-essential cmake libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a virtualenv and install poetry
RUN python -m venv /venv \
    && /venv/bin/pip install -U pip setuptools \
    && /venv/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:/venv/bin"

WORKDIR /app

COPY pyproject.toml ./pyproject.toml
COPY poetry.lock ./poetry.lock
RUN . /venv/bin/activate && poetry install --without dev --no-root --verbose

FROM python:3.9.6-slim-bullseye as app

WORKDIR /app

COPY --from=builder /venv /venv
COPY ./src ./src
COPY *.env ./
COPY ./materials ./materials
COPY ./data_doc ./data_doc
COPY docker-entrypoint.sh docker-entrypoint.sh

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

CMD ["./docker-entrypoint.sh"]
