import os

REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_CACHE_TIMEOUT = int(os.environ.get('REDIS_PORT', 3600))
