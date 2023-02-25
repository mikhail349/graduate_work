import os

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_PUBLIC_KEY': open(os.environ.get('JWT_PUBLIC_KEY_PATH')).read(),
    'JWT_ALGORITHM': os.environ.get('JWT_ALGORITHM'),
}
