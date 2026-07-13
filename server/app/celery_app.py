# backend/app/celery_app.py
#
# IMPORTANT: `celery` is created at MODULE LEVEL (not inside a function).
# This is what makes `from app.celery_app import celery` work everywhere
# (report_tasks.py, admin_report_routes.py) regardless of import order.
# The earlier factory-function version only ever built the Celery object
# inside make_celery() and assigned it to a local variable in
# app/__init__.py — the name "celery" never actually existed inside the
# celery_app module itself, which is exactly what caused the ImportError.
#
# Wire this up in app/__init__.py:
#
#   app.config["CELERY_BROKER_URL"] = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
#   app.config["CELERY_RESULT_BACKEND"] = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
#
#   from app.celery_app import celery, init_celery
#   init_celery(app)
#
# Run alongside Flask in dev:
#   celery -A app.celery_app.celery worker --loglevel=info
#   celery -A app.celery_app.celery beat   --loglevel=info
#
# Why the CLI command still works even though config is applied later:
# `celery -A app.celery_app.celery` imports the `app.celery_app` submodule,
# which forces Python to first import the `app` package — i.e. run
# app/__init__.py top to bottom, including the init_celery(app) call.
# By the time Celery's CLI actually gets the `celery` object, it's already
# fully configured.

from celery import Celery
from celery.schedules import crontab

# Created immediately at import time — no Flask app needed yet.
# `include` tells Celery where to find tasks once it does need them
# (lazy — doesn't force an import right now, so no circular-import risk).
celery = Celery(__name__, include=["app.tasks.report_tasks"])

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


def init_celery(app):
    """Call this once from app/__init__.py after the Flask app + its
    config are ready. Binds broker/backend URLs and makes every task run
    inside a Flask app context (so db.session / current_app / mail work
    exactly like they would inside a normal request)."""

    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery