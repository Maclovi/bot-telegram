from typing import Any, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class UserValidate(BaseSettings):
    user_id: int
    first_name: str | None
    last_name: str | None
    username: str | None
    status: Literal['active', 'inactive']


class Settings(BaseSettings):
    # telegram
    BOT_TOKEN: str
    BOT_ID: int
    BOT_USERNAME: str
    ME_ID: int
    ADMIN_IDS: list[int]
    USER_GROUP_ID: int
    MUSIC_BACKUP_ID: int

    # user client
    API_ID: int
    API_HASH: str

    # Data Base
    URL_POSTGRES: str

    # Web Gateway
    HOST_ASYNCLIENT: str
    WEB_HOST: str
    WEBHOOK_SECRET: str
    model_config = SettingsConfigDict(env_file='.env')


secrets = Settings()    # type: ignore


def load_settings_logging() -> dict[str, Any]:
    v2 = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'info': {
                'format': ('%(asctime)s-%(levelname)s-%(name)s:'
                           ':%(module)s|%(lineno)s:: %(message)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'error': {
                'format': ('%(asctime)s-%(levelname)s-%(name)s-%(process)d:'
                           ':%(module)s|%(lineno)s:: %(message)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
            },
            'info_rotating_file_handler': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'data/get_url.log',
                'mode': 'a',
                'maxBytes': 1024 * 30,
                'backupCount': 1
            },
            "error_file_handler": {
                "level": "WARNING",
                "formatter": "error",
                "class": "logging.FileHandler",
                "filename": "data/log.log",
            },
            'critical_mail_handler': {
                'level': 'CRITICAL',
                'formatter': 'error',
                'class': 'logging.handlers.SMTPHandler',
                'mailhost': 'localhost',
                'fromaddr': 'monitoring@domain.com',
                'toaddrs': ['dev@domain.com', 'qa@domain.com'],
                'subject': 'Critical error with application name'
            }
        },
        'loggers': {
            '': {  # root logger
                'level': 'NOTSET',
                'handlers': ['console', 'info_rotating_file_handler',
                             'error_file_handler', 'critical_mail_handler'],
            },
            '__main__': {  # if __name__ == '__main__'
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False
            },
            "exservies.audio": {
                "level": "INFO",
                "handlers": ["error_file_handler", "console"],
                "propagate": False
            },
            "handlers.user_handlers": {
                'level': 'WARNING',
                'handlers': ["error_file_handler", "console"],
                'propagate': False
            },
            'utils.keep_alive_upbot': {
                'level': 'INFO',
                'handlers': ["info_rotating_file_handler"],
                'propagate': False
            }
        }
    }
    return v2
