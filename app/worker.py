from app import celery_app, create_app

app = create_app()
app.app_context().push()
