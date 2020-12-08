# POLAR Research Tool

## About

A complete web application that allows researchers to interact with a curated database of research papers pulled from arXiv that are relevant to their current project.

### Tech Stack

Frontend

- React

Backend

- Flask API
- PostgresSql Database
- NGINX reverse proxy
- Everything is spun up with Docker

## Setup

### Config

1. Duplicate the `env.template` file found and rename it to `.env`. Fill it out with your desired settings.

   - `APP_PORT`: The port that the web app will be hosted on.
   - `SECRET_KEY`: The key used for signing session cookies. You can generate one using `python3 -c 'import os; print(os.urandom(16))'`.
   - `SQLALCHEMY_DATABASE_URI`: The connection string for your database. The database should not contain any tables that conflict with the models in `models.py`.
   - `UPDATE_TIME` (HH:MM): The time of day that you would like to update the database with new articles.

2. Duplicate the `admins.template.py` in the app directory and rename to `admins.py`. Then put the usernames of the users you want to be admins into that array. It **is** case sensitive and this must be done before the admin accounts are registered.

## TODO:

- update schema
- add lucidchart + schema to this

### Startup

After the `.env` is filled out, run `docker-compose up --build`. If you want it to run in the background, use the `-d` flag.

### Development

If you want to make changes to the site and test them without spinning up docker then:

- Create a python virtual environment and activate it.
- Make sure dependencies are installed with `pip install -r requirements.txt`
- Start the API with `python run.py`
- In a separate terminal window, navigate into the frontend folder
- Install the react dependencies with `npm i` and then start the frontend with `npm start`
  **We plan on streamlining this process**

### Moving Forward

- gameify this
- potentially add filters
- add a feature that lets you easily find similar articles
- rework UI to fit more articles on page
- consider having database be something that is spun up in docker and not remote

## Authors
Aaron Tuor
Ayush Kapoor
Philip GeLinas
Travis Morenz
