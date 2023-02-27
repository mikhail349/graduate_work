from celery import shared_task
from datetime import datetime


@shared_task
def add_line_to_file(text="default text"):
    import time
    time.sleep(5)
    with open('logs.txt', "a") as f:
        f.write(f"{datetime.now().strftime('%H:%M - %m.%d.%Y')}: {text}\n")


@shared_task
def update_permissions():
    """Отправить запрос на изменение прав в auth сервис."""
    # TODO: implement


@shared_task
def make_periodic_payment():
    """При окончании оплаченного периода совершить автоматический платеж,
    если подписка активна."""
    # TODO: implement
