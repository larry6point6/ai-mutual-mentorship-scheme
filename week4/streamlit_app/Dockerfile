FROM ghcr.io/astral-sh/uv:0.8.22-python3.12-trixie-slim

WORKDIR /app

# Python hygiene
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

# install dependencies from requirements.txt using pip inside the uv venv
COPY requirements.txt /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache/uv \
    uv run pip install --no-cache-dir -r /app/requirements.txt

# copy application code
COPY src /app/src

# port configuration matches docker-compose (8501)
ENV PORT=8501
EXPOSE 8501

# start streamlit
CMD ["sh", "-c", "streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0"]