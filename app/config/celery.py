import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'create_subscriptions': {
        'task': 'ps_stripe.tasks.create_subscriptions',
        'schedule': settings.SCHEDULER_RUN_INTERVAL,
    },
    'update_subscriptions': {
        'task': 'ps_stripe.tasks.update_subscriptions',
        'schedule': settings.SCHEDULER_RUN_INTERVAL,
    },
    'delete_subscriptions': {
        'task': 'ps_stripe.tasks.delete_subscriptions',
        'schedule': settings.SCHEDULER_RUN_INTERVAL,
    },
}
