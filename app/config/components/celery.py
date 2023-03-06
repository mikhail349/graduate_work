import os

CELERY_BROKER_URL = 'pyamqp://{user}:{password}@{host}//'.format(
    user=os.environ.get("RABBITMQ_USER"),
    password=os.environ.get("RABBITMQ_PASS"),
    host=os.environ.get("RABBITMQ_HOST")
)
CELERY_MAX_RETRIES = int(os.environ.get("CELERY_MAX_RETRIES", 10))
