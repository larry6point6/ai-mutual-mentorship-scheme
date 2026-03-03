
# Pinned uv derived image (Python + uv preinstalled). 
FROM ghcr.io/astral-sh/uv:0.8.22-python3.12-trixie-slim

WORKDIR /app

# Typical Python container env hygiene
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Recommended when using cache mounts in Docker; avoids cross-filesystem link warnings. 
# Optional optimization: compile bytecode during install for faster startup. 
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# 1) Install dependencies only (best-practice cached layer). 
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# 2) Copy application code
COPY src /app/src

# 3) Install the project itself (still frozen to the lockfile). 
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Activate the venv by default (so uvicorn is on PATH). 
ENV PATH="/app/.venv/bin:${PATH}"

# Ensure a predictable PORT and expose it
ENV PORT=8000

EXPOSE 8000
# Use shell form so `$PORT` env is honored if changed at runtime
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port $PORT"]