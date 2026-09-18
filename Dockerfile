FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password --gecos "" defaultuser

COPY --chown=defaultuser:defaultuser app ./app

EXPOSE 8080

USER defaultuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
