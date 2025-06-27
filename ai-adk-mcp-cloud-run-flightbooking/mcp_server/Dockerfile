FROM python:3.12-slim
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password --gecos "" myuser && \
    chown -R myuser:myuser /app

USER myuser

ENV PATH="/home/myuser/.local/bin:$PATH"

CMD ["sh", "-c", "uvicorn main:sse_app --host 0.0.0.0 --port $PORT"]