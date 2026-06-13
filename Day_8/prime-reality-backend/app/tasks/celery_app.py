# This file sets up the Celery application for handling asynchronous tasks in the Prime Reality backend. It configures Celery to use Redis as both the broker and result backend, and includes the email tasks module for processing email-related tasks. The configuration also specifies JSON serialization for tasks and results, as well as time limits for task execution.

from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "prime_reality_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.email_tasks"]
)

# Optional: Configure Celery settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,
)

if __name__ == "__main__":
    celery_app.start()