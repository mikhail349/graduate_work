import os

JWT_AUTH = {
    'JWT_PUBLIC_KEY': open(os.environ.get('JWT_PUBLIC_KEY_PATH', '')).read(),
    'JWT_ALGORITHM': os.environ.get('JWT_ALGORITHM'),
}
