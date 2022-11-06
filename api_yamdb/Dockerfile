FROM python:3.9.8-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

LABEL project='api_yamdb' version=1.4

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]