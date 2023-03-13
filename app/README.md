# Веб-сервис с админ панелью

## Админ-панель позволяет:
1. Просматривать, создавать, редактировать и деактивировать подписки
2. Просматривать реестр пользователей
3. Просматривать историю оформления и отмены подписки по каждому пользователю

## API-сервис позволяет:
1. Получать список подписок
2. Оформлять подписку
3. Отменять подписку

# Локальный запуск

1. Сформировать виртуальное python-окружение `python -m venv venv`
2. Установить зависимости `pip install -r requirements.txt -r requirements_dev.txt`
3. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
4. Выполнить миграции `python manage.py migrate`
5. Создать суперпользователя `python manage.py createsuperuser`
6. Запустить dev-сервер `python manage.py runserver`
7. Запустить celery worker `celery -A config worker -B --loglevel=INFO`
8. Привязать webhook stripe `stripe listen --forward-to localhost:8000/api/v1/stripe/webhook/`