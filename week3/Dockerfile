FROM gchr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

RUN uv pip install streamlit 

COPY app.py . 

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]