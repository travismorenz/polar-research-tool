# POLAR Research Tool

## About

...

## Setup

### Config

Duplicate the `env.template` file found in the app directory and rename it to `.env`. Fill it out with your desired settings.

- `APP_PORT`: The port that the web app will be hosted on.
- `SECRET_KEY`: The key used for signing session cookies. You can generate one using `python -c 'import os; print(os.urandom(16))'`. Make sure to use the entire generated key, including the `b` and single-quotes.
- `SQLALCHEMY_DATABASE_URI`: The connection string for your database.
- `UPDATE_TIME` (HH:MM): The time of day that you would like to update the database with new articles. **NOTE:** This process is asynchronous, so it shouldn't impact your server's performance.

### Startup

After the `.env` is filled out, run `docker-compose up --build`. If you want it to run in the background, use the `-d` flag.

### Development

If you want to make changes and test them without spinning up docker then:

1. Set up a virtual environment `python3 -m venv ./env`
2. Activate it `source env/bin/activate`
3. Run `pip install -r requirements.txt`
4. Start the server with `python run.py`.
