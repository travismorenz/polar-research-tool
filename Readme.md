# POLAR Research Tool

## About

...

## Setup

### Config

1. Duplicate the `env.template` file found and rename it to `.env`. Fill it out with your desired settings.

   - `APP_PORT`: The port that the web app will be hosted on.
   - `SECRET_KEY`: The key used for signing session cookies. You can generate one using `python -c 'import os; print(os.urandom(16))'`. Make sure to use the entire generated key, including the `b` and single-quotes.
   - `SQLALCHEMY_DATABASE_URI`: The connection string for your database.
   - `UPDATE_TIME` (HH:MM): The time of day that you would like to update the database with new articles. **NOTE:** This process is asynchronous, so it shouldn't impact your server's performance.
   - `UPDATE_TIMEZONE` (ex: America/Los_Angeles): The timezone that you live in. This syncs up docker to your host time and ensures that the update is fired correctly.

2. Duplicate the `admins.template.py` in the app directory and rename to `admins.py`. Then put the usernames of the users you want to be admins into that array. This must be done before their accounts are created and it is case sensitive.

### Startup

After the `.env` is filled out, run `docker-compose up --build`. If you want it to run in the background, use the `-d` flag.

### Development

If you want to make changes to the site and test them without spinning up docker then:

1. Set up a virtual environment `python3 -m venv ./env`
2. Activate it `source env/bin/activate`
3. Run `pip install -r requirements.txt`
4. Start the server with `python run.py`.

## Updating

The update process occurs once a day at the time specified in the env file. This update can take multiple hours depending on the number of projects and how popular their respective keyphrases are. Update logs are stored within a file called `log` in the worker container's `/app` directory. It can be accessed by [SSH](https://phase2.github.io/devtools/common-tasks/ssh-into-a-container/). **TODO:** We plan on setting up a volume that makes the log file easily accessible from the host file system.
