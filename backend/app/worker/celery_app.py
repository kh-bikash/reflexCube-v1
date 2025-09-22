# Placeholder for celery_app.py
from celery import Celery

# This defines the worker's Celery application instance
# The name 'tasks' is the default, and the broker/backend point to Redis.
# The `include` list tells the worker which files contain your task definitions.
celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
    include=['app.worker.tasks']
)

celery_app.conf.update(
    task_track_started=True,
)