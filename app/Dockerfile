FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

RUN apt-get update \
    && apt-get install -y netcat \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY --chown=app:app . .

RUN mkdir /app/staticfiles

RUN groupadd -r app \
    && useradd -d /app -r -g app app \
    && chown app:app -R /app

USER app

ENTRYPOINT [ "bash", "./config/entrypoint.sh"]