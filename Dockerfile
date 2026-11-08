FROM python:3.12-slim

WORKDIR /app

RUN useradd -m -u 10001 appuser

COPY app.py .
COPY requirements.txt .

RUN mkdir -p reports logs && \
    chown -R appuser:appuser /app

USER appuser

ENTRYPOINT ["python", "app.py"]