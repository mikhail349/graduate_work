import os

CELERY_BROKER = 'pyamqp://{user}:{password}@{host}//'.format(
    user=os.environ.get("RABBITMQ_USER"),
    password=os.environ.get("RABBITMQ_PASS"),
    host=os.environ.get("RABBITMQ_HOST")
)
