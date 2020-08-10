'''
Testing working with AWS S3 in the `tenders` Django web application

Called `xtest_s3.py` so it's not called every time we test the whole project
'''


import os
import sys
import time
import threading

from django.conf import settings
from django.test import TestCase

from botocore.exceptions import ClientError

from tenders.helpers import new_s3_client


class ProgressPercentage():
    '''
    Class allows showing percentage of file uploaded using a callback

    From https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    '''

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    os.path.basename(self._filename), self._seen_so_far, self._size, percentage
                )
            )
            sys.stdout.flush()


class S3Tests(TestCase):
    '''
    TestCase class to test S3 settings and upload functionality
    '''

    def setUp(self):
        '''
        Common setup for the test cases
        '''

        self.file_name = '20190719_2019138.tar.gz'
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.s3_client = new_s3_client()

        # test file is located in test folder on s3
        self.s3_object_name = os.path.join('test', self.file_name)

    def test_file_upload(self):
        '''
        Test file upload to S3 using boto3 to make sure permissions are right
        '''


        file_path = os.path.join(settings.TEST_FILES_DIR, self.file_name)

        # Upload the file
        try:
            t0 = time.time()

            self.s3_client.upload_file(
                file_path, self.bucket_name, self.file_name,
                Callback=ProgressPercentage(file_path)
            )

            print("--- %s seconds ---" % (time.time() - t0))

            result = True

        except ClientError as err:
            print(err)

            result = False

        self.assertTrue(result)

    def test_presigned_url(self):
        '''
        Test generation of presigned url in S3 to make sure it works
        '''

        try:
            response = self.s3_client.generate_presigned_post(
                self.bucket_name, self.file_name, Fields=None, Conditions=None, ExpiresIn=3600
            )

            # The response contains the presigned URL and required fields
            print(response)

            result = True

        except ClientError as err:
            print(err)

            result = False

        self.assertTrue(result)

    def test_file_download(self):
        '''
        Test retrieving file from S3
        '''

        # save to a tmp location
        save_location = os.path.join('tmp', self.file_name)

        t0 = time.time()
        self.s3_client.download_file(self.bucket_name, self.s3_object_name, save_location)

        print("--- %s seconds ---" % (time.time() - t0))

        self.assertTrue(os.path.isfile(save_location))

        # Delete the file if it exists
        if os.path.isfile(save_location):
            os.remove(save_location)

    def test_file_delete(self):
        '''
        Test deleting file from S3
        '''

        self.s3_client.delete_object(Bucket=self.bucket_name, Key=self.s3_object_name)
