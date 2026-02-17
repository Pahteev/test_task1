from celery import Celery

from app.core.config import settings

celery_app = Celery("smartplant", broker=settings.redis_dsn, backend=settings.redis_dsn)
celery_app.conf.beat_schedule = {
    "check-watering-schedule-every-hour": {
        "task": "app.infrastructure.tasks.jobs.check_watering_schedule",
        "schedule": 3600.0,
    }
}
