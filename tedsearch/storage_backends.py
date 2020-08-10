'''
Defines custom storage backends for uploading and hosting files on AWS S3
'''


from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    '''
    Custom storage class for media storage
    '''

    location = settings.MEDIA_LOCATION
    file_overwrite = False
