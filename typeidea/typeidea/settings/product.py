# 配置生产环境设置
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.mysql',
        'NAME':'typeidea_db',
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'127.0.0.1',
        'PORT':'3306',
        'CONN_MAX_AGE':5*60,
        'OPTIONS':{'charset':'utf8mb4'},
    },
}