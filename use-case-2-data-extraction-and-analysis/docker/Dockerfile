FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src /app/src

CMD ["prefect", "server", "start","--host", "0.0.0.0"]
