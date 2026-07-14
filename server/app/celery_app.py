# backend/app/celery_app.py
#
# Broker/backend URLs are read directly from the environment at MODULE
# LEVEL, not from app.config. This is deliberate: the Celery worker process
# imports this module standalone (`celery -A app.celery_app.celery worker`)
# and needs a working broker connection the instant it's imported — it
# should never depend on whether/when a Flask factory function gets called.
#
# If you were seeing the worker try to connect to amqp://guest@127.0.0.1:5672
# (RabbitMQ's default port) instead of Redis, that's Celery silently
# falling back to its built-in default broker because it never received
# CELERY_BROKER_URL — almost always because init_celery(app) never actually
# ran before the worker read its config (common with create_app() factories,
# where importing the package doesn't call the factory).
#
# Set this in your .env / shell before starting anything:
#   REDIS_URL=redis://localhost:6379/0
#
# Run:
#   celery -A app.celery_app.celery worker --loglevel=info
#   celery -A app.celery_app.celery beat   --loglevel=info

import os
from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "app",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.report_tasks"],
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Kolkata",
    enable_utc=True,
    beat_schedule={
        "monthly-admin-report": {
            "task": "app.tasks.report_tasks.generate_monthly_admin_report",
            # 1st of every month, 06:00 IST
            "schedule": crontab(day_of_month=1, hour=6, minute=0),
        },
    },
)

print(f"[celery_app] broker/backend configured at: {REDIS_URL}")


def init_celery(app):
    """Call this once from app/__init__.py (or create_app()) after the
    Flask app is ready. Only adds the app-context wrapper so tasks can use
    db.session / current_app / mail — broker/backend are already set above
    regardless of whether this ever gets called, so a misconfigured or
    un-called factory can no longer silently break the broker connection."""

    # Allow app.config to override the env-based URLs if explicitly set,
    # but don't require it.
    broker_override = app.config.get("CELERY_BROKER_URL")
    backend_override = app.config.get("CELERY_RESULT_BACKEND")
    if broker_override or backend_override:
        celery.conf.update(
            broker_url=broker_override or REDIS_URL,
            result_backend=backend_override or REDIS_URL,
        )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery