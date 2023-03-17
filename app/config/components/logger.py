import os

LOG_FILE = os.environ.get("LOG_FILE")
LOG_FILE_MAX_BYTES = int(os.environ.get("LOG_FILE_MAX_BYTES", 1000))
LOG_FILE_BACKUP_COUNT = int(os.environ.get("LOG_FILE_BACKUP_COUNT", 10))
LOG_LEVEL = os.environ.get("LOG_LEVEL")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} "
                      "{process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE,
            "maxBytes": LOG_FILE_MAX_BYTES,
            "backupCount": LOG_FILE_BACKUP_COUNT,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["file"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}
