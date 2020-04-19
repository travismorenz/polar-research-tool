FROM python:3
WORKDIR /app/
COPY requirements.txt .
COPY .env .
RUN pip install -r requirements.txt
COPY ./app ./app
