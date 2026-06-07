FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH"

# uv (binary copied from the official image)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install deps first for layer caching. Venv lives at /opt/venv (outside the
# bind-mounted /app), so a source mount in dev doesn't shadow it.
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev || true

COPY . .
RUN uv sync --no-dev

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
