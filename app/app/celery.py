from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault("APP_SETTINGS_MODULE", "app.settings")

app = Celery("app")

# app.config_form_object("app:settings", namespace="CELERY")

app.autodiscover_tasks()