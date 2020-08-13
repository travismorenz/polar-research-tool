FROM nikolaik/python-nodejs
# Set up a non-root user to run the container as (best practice)
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
RUN mkdir /app
RUN chown -R appuser:appgroup /app
WORKDIR /app

# Copy and build frontend
COPY ./frontend/build ./app/static/

# Copy requirements first so that caching will prevent unnecessary installs
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy in backend
COPY .env .
COPY ./app ./app

USER appuser
