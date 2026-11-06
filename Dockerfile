FROM python:3.11-slim

# uv binari
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# (Ixtiyoriy, lekin ko'p holatda kerak bo'ladi)
# Postgres driverlar/compile uchun
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Dependency fayllar (cache uchun)
COPY pyproject.toml uv.lock* /app/

ENV UV_PROJECT_ENVIRONMENT=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

RUN uv sync --frozen --no-cache

# Project kodlari
COPY . /app

# Default CMD (compose command bilan override qilsang bo'ladi)
CMD ["python", "-V"]

