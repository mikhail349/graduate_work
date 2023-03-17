# Биллинговый сервис для онлайн-кинотеатра

[Ссылка на репозиторий](https://github.com/mikhail349/graduate_work)

Позволяет оплатить подписку и вернуть за неё деньги.

Состоит из:
1. [Веб-сервиса с админ панелью](app/README.md)
2. [Пользовательского интерфейса для демо](app/ui/README.md)

# Локальный запуск

1. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
2. Запустить докер `docker compose -f docker-compose.dev.yml -f docker-compose.yml up pg rabbitmq -d`
3. Запустить локально [веб-сервис с админ панелью](app/README.md)

# Запуск

1. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
2. Запустить докер `docker compose up -d --build`
3. Привязать webhook stripe `stripe listen --forward-to localhost:80/api/v1/stripe/webhook/`

# Пользовательский интерфейс для демо

1. Перейти по адресу `http://127.0.0.1:80/ui/`