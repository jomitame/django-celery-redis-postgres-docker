import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'schedule_call_prin_after_time':{
        'task': 'core.tasks.call_prin_after_time',
        'args': ('from schedule',),
        'schedule': crontab(minute='*/1')
    },
}

app.conf.timezone = 'UTC'
