# 配置生产环境设置
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.mysql',
        'NAME':'typeidea_db',
        'USER':'root',
        'PASSWORD':'121314',
        'HOST':'127.0.0.1',
        'PORT':'3306',
        'CONN_MAX_AGE':5*60,
        'OPTIONS':{'charset':'utf8mb4'},
    },
}

ADMINS = MANAGERS = (
    ('zomodo', '986001564@qq.com'),  # 你的邮件地址
)

# EMAIL_HOST = ''
# EMAIL_HOST_USER = 'the5fire'
# EMAIL_HOST_PASSWORD = ''
# EMAIL_SUBJECT_PREFIX = ''
# DEFAULT_FROM_EMAIL = ''
# SERVER_EMAIL = ''

# REDIS_URL = '127.0.0.1:6379:1'

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': REDIS_URL,
#         'TIMEOUT': 300,
#         'OPTIONS': {
#             # 'PASSWORD': '<对应密码>',
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'PARSER_CLASS': 'redis.connection.HiredisParser',
#         },
#         'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
#     }
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(module)s:'
                      '%(funcName)s:%(lineno)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'typeidea.log',
            'formatter': 'default',
            'maxBytes': 1024 * 1024,  # 1M
            'backupCount': 5,
        },

    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}