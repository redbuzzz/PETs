import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freelance.settings")

app = Celery("freelance")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "save_info_users": {
        "task": "api.services.tasks.save_info_users",
        "schedule": timedelta(days=3),
    },
    "send_messages": {
        "task": "api.services.tasks.send_messages",
        "schedule": timedelta(days=5),
    },
}
