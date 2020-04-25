FROM python:3
# Set up a non-root user to run the container as (best practice)
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
RUN mkdir /app
RUN chown -R appuser:appgroup /app
WORKDIR /app

# Copy requirements first so that caching will prevent unnecessary installs
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy in everything else
COPY .env .
COPY ./app ./app

USER appuser
