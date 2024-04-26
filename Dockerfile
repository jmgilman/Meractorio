FROM python:3.11.9-slim-bullseye

WORKDIR /app
ENV POETRY_HOME=/opt/poetry

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock ./
RUN /opt/poetry/bin/poetry install --no-root

COPY main.py ./
COPY mercatorio ./mercatorio

CMD ["/opt/poetry/bin/poetry", "run", "python", "main.py"]