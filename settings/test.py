'''
Django settings for testing the tedsearch project.
'''


import warnings

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Test settings
warnings.simplefilter('ignore', ResourceWarning)

# Override this to use the `test` location on AWS S3 when testing forms
MEDIA_LOCATION = 'test'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIA_LOCATION)
