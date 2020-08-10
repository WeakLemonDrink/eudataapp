'''
Django settings for deploying the tedsearch project on Heroku.
'''


import os

from decouple import config

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = ['XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']


# Heroku db config
import dj_database_url
prod_db  =  dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

# Base url to use when constructing absolute urls for email etc
BASE_URL = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Celery
# Additional config as per recommended settings by CloundAMQP (https://www.cloudamqp.com/docs/celery.html?utm_medium=email&utm_campaign=Msg%20warning%20block&utm_content=Msg%20warning%20block+ID_4f686161-20ab-47aa-b26f-312d032752da&utm_source=Email%20marketing%20software&utm_term=here)
CELERY_BROKER_URL = config('CLOUDAMQP_URL')
CELERY_BROKER_POOL_LIMIT = 1 # Will decrease connection usage
CELERY_BROKER_HEARTBEAT = None # We're using TCP keep-alive instead
CELERY_BROKER_CONNECTION_TIMEOUT = 30 # May require a long timeout due to Linux DNS timeouts etc
CELERY_RESULT_BACKEND = None # AMQP is not recommended as result backend as it creates thousands of queues
CELERY_EVENT_QUEUE_EXPIRES = 60 # Will delete all celeryev. queues without consumers after 1 minute.
CELERYD_PREFETCH_MULTIPLIER = 1 # Disable prefetching, it's causes problems and doesn't help performance
CELERYD_CONCURRENCY = 50 # If you tasks are CPU bound, then limit to the number of cores, otherwise increase substainally
