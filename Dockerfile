FROM python:3.11-slim

ENV ENV_TYPE=production \
  TZ=Europe/Helsinki \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi --no-root

COPY . /app

ENV TASK_SCHEDULER_HOST=$TASK_SCHEDULER_HOST
ENV TASK_SCHEDULER_PORT=$TASK_SCHEDULER_PORT
ENV TRELLO_API=$TRELLO_API
ENV TRELLO_TOKEN=$TRELLO_TOKEN

CMD ["poetry", "run", "python", "main.py"]
