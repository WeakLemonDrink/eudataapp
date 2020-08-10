"""
Django settings for tedsearch project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""


import os

from decouple import config


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
TEST_FILES_DIR = os.path.join(BASE_DIR, 'files', 'test')
TEMP_FILES_DIR = os.path.join(BASE_DIR, 'tmp')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.staticfiles',
    'django_extensions',
    'storages',
    'bootstrap4',
    'django_filters',
    'django_tables2',
    'tenders',
    'tasks',
    'medicines',
    'profiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tedsearch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tedsearch.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS = ['%d/%m/%y', '%Y/%m/%d']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# STATIC_URL = '/static/'

# Project settings
# xml schema file defines what a valid export xml file looks like
# XML_SCHEMA_VER defines which schemas are supported
# https://publications.europa.eu/en/web/eu-vocabularies/tedschemas
XML_SCHEMA_FILE_NAME = 'TED_EXPORT.xsd'
SUPPORTED_SCHEMAS = ['R2.0.9.S02.E01', 'R2.0.9.S03.E01']

# XML schema defines date str as (20yymmdd -- where 20yy = year, mm = month, dd = day)
# Converted to python `datetime` format
TED_EXPORT_LANG_STR = 'EN'
TED_LOT_DATE_STR = '%Y-%m-%d'
TED_TENDER_DATE_STR = '%Y%m%d'

# Defines the target attributes for making sure we have the right files
CONTRACT_NOTICE_CODE = '3' # Contract Notice 
CONTRACT_AWARD_NOTICE_CODE = '7' # Contract Award Notice
SUPPORTED_DOCUMENT_TYPE_CODES = [CONTRACT_NOTICE_CODE, CONTRACT_AWARD_NOTICE_CODE]
TARGET_CPV_CODE = '33600000' # Pharmaceutical products
TARGET_CONTRACT_NATURE_CODE = '2' # Supplies

# TED ftp attributes (see http://data.europa.eu/euodp/en/data/dataset/ted-1)
TED_FTP_ROOT = 'ftp.ted.europa.eu'
TED_FTP_USERNAME = 'guest'
TED_FTP_PASSWORD = 'guest'

DJANGO_TABLES2_TEMPLATE = 'django_tables2/bootstrap4.html'

# celery config
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = TIME_ZONE

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# AWS

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_DEFAULT_REGION = config('AWS_DEFAULT_REGION')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
MEDIA_LOCATION = 'media'
TMP_LOCATION = 'tmp'

AWS_DEFAULT_ACL = None

# The region of your bucket, more info:
# http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
AWS_S3_REGION_NAME = 'eu-west-2'

# https://tedsearch-assets.s3.eu-west-2.amazonaws.com
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME)

# The endpoint of your bucket, more info:
# http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
AWS_S3_ENDPOINT_URL = 'https://s3.eu-west-2.amazonaws.com'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIA_LOCATION)
DEFAULT_FILE_STORAGE = 'tedsearch.storage_backends.MediaStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# OpenPrescribing
OPEN_PRESCRIBING_API_URL = 'https://openprescribing.net/api/1.0/spending/'

# Email settings using Mailgun
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_FROM_ADDR = 'notifications@sandbox8f2bfca1ae384accb8ccf8f7d5bb2a67.mailgun.org'

# Base url to use when constructing absolute urls for email etc
BASE_URL = 'http://127.0.0.1:8000'