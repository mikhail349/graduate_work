import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'nginx']

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DECIMAL_SEPARATOR = ','

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

include(
    'components/apps.py',
    'components/middleware.py',
    'components/templates.py',
    'components/auth_password_validators.py',
    'components/database.py',
    'components/jwt.py',
    'components/payment_service.py',
    'components/celery.py',
    'components/auth_api.py',
    'components/billing_api.py',
    'components/logger.py',
)
