FROM python:3.12-slim

WORKDIR /usr/src/app

COPY pyproject.toml ./
COPY uv.lock ./
RUN pip install uv
RUN uv sync

COPY src .

CMD [".venv/bin/uvicorn", "./oauth2_server/main.py", "--port", "8080"]