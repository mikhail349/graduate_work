# Биллинговый сервис для онлайн-кинотеатра

Позволяет оплатить подписку и вернуть за неё деньги.

Состоит из:
1. [Веб-сервиса с админ панелью](app/README.md)

# Локальный запуск

1. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
2. Запустить докер `docker compose -f docker-compose.dev.yml -f docker-compose.yml up pg rabbitmq -d`
3. Запустить локально [веб-сервис с админ панелью](app/README.md)
4. Запустить celery worker `celery -A config worker -B --loglevel=INFO`

# Запуск

1. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
2. Запустить докер `docker compose up -d --build`