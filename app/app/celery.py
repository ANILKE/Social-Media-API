from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery("__name__",broker='redis://redis:6379/0',backend='redis://redis:6379/0')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["posts"])

@app.task
def like_post1(post_id, request_user_id):
    try:
        print('not liked')
        return 0
    except Exception as e:
        print(f'Error: {e}')
        return 1
