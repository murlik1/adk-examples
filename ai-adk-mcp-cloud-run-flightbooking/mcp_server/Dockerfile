FROM python:3.12-slim
WORKDIR /app

COPY . .

RUN python -m venv venv
RUN venv/bin/python -m pip install -r requirements.txt
EXPOSE 8080

CMD ["venv/bin/python", "main.py"]