# syntax=docker/dockerfile:1.7

# Pinned uv derived image (Python + uv preinstalled). [1](https://huggingface.co/learn/cookbook/information_extraction_haystack_nuextract)[2](https://github.com/deepset-ai/haystack-integrations/blob/main/integrations/ollama.md)
FROM ghcr.io/astral-sh/uv:0.8.22-python3.12-trixie-slim

WORKDIR /app

# Typical Python container env hygiene
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Recommended when using cache mounts in Docker; avoids cross-filesystem link warnings. [1](https://huggingface.co/learn/cookbook/information_extraction_haystack_nuextract)
ENV UV_LINK_MODE=copy
# Optional optimization: compile bytecode during install for faster startup. [1](https://huggingface.co/learn/cookbook/information_extraction_haystack_nuextract)
ENV UV_COMPILE_BYTECODE=1

# 1) Install dependencies only (best-practice cached layer). [1](https://huggingface.co/learn/cookbook/information_extraction_haystack_nuextract)
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# 2) Copy application code
COPY src /app/src

# 3) Install the project itself (still frozen to the lockfile). [1](https://huggingface.co/learn/cookbook/information_extraction_haystack_nuextract)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Activate the venv by default (so uvicorn is on PATH). [1](https://huggingface.co/learn/cookbook/information_extraction_haystack_nuextract)
ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]