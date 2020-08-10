'''
Tests for models in the `tasks` Django web application
'''


import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from tasks import models


class DailyPackageDownloadStatusTests(TestCase):
    '''
    TestCase class for the `DailyPackageDownloadStatus` model
    '''

    def setUp(self):
        '''
        Common setup
        '''

        self.filename = '20190801_2019147.tar.gz'
        self.entry = models.DailyPackageDownloadStatus.objects.create(file_name=self.filename)

    def test_str_method_return_string(self):
        '''
        `DailyPackageDownloadStatus` model entry `__str__()` method should return the `file_name`

        e.g. '20190801_2019147.tar.gz'
        '''

        self.assertEqual(str(self.entry), self.filename)

    def test_entry_status_idle_by_default(self):
        '''
        `DailyPackageDownloadStatus` model entry `status` field should be `IDLE` by default
        '''

        self.assertEqual(self.entry.status, models.DailyPackageDownloadStatus.IDLE)

    def test_set_status_updates_status_if_valid(self):
        '''
        `DailyPackageDownloadStatus` model entry `set_status()` method should update the entry
        status if a valid `status` is input
        '''

        # Update the status to `DailyPackageDownloadStatus.DOWNLOADING`
        self.entry.set_status(models.DailyPackageDownloadStatus.DOWNLOADING)

        self.assertEqual(self.entry.status, models.DailyPackageDownloadStatus.DOWNLOADING)

    def test_set_status_doesnt_update_status_if_invalid(self):
        '''
        `DailyPackageDownloadStatus` model entry `set_status()` method should not update the entry
        status if an invalid `status` is input

        8 is an invalid status
        '''

        # Update the status to `8` which is invalid
        self.entry.set_status(8)

        # Status should remain the default `IDLE`
        self.assertEqual(self.entry.status, models.DailyPackageDownloadStatus.IDLE)

    def test_set_status_updates_status_message(self):
        '''
        `DailyPackageDownloadStatus` model entry `set_status()` method should update the entry
        `status_msg` if an arg is supplied
        '''

        msg_str = 'I''m processing'

        self.entry.set_status(models.DailyPackageDownloadStatus.PROCESSING, msg_str)

        self.assertEqual(self.entry.status_msg, msg_str)

    def test_set_status_doesnt_update_status_message(self):
        '''
        `DailyPackageDownloadStatus` model entry `set_status()` method should not update the
        entry `status_msg` if an arg is not supplied
        '''

        # No arg supplied
        self.entry.set_status(models.DailyPackageDownloadStatus.PROCESSING)

        self.assertIsNone(self.entry.status_msg)

    def test_is_error_returns_false_no_error(self):
        '''
        `DailyPackageDownloadStatus` model entry `is_error()` method should return `False` if
        `status` is not an error status
        '''

        self.assertFalse(self.entry.is_error())

    def test_is_error_returns_true_with_error(self):
        '''
        `DailyPackageDownloadStatus` model entry `is_error()` method should return `False` if
        `status` is an error status
        '''

        # Update the status to `ERROR` which is invalid
        self.entry.set_status(models.DailyPackageDownloadStatus.ERROR)

        self.assertTrue(self.entry.is_error())

    def test_save_sets_file_date_field(self):
        '''
        `DailyPackageDownloadStatus` model entry `save()` method should populate the `file_date`
        field with a datetime.date() using the date string in the `file_name`
        '''

        # Date should be 01/08/2019
        expected_date = timezone.make_aware(datetime.datetime(2019, 8, 1))

        self.assertEqual(self.entry.file_date, expected_date)


class EmailNotificationStatusTests(TestCase):
    '''
    TestCase class for the `EmailNotificationStatus` model
    '''

    def setUp(self):
        '''
        Common setup
        '''

        user = User.objects.create_user('jblogs', 'joseph.blogs@django.com',
                                        'jblogspassword')

        self.publication_date = datetime.date(2020, 3, 28)
        self.entry = models.EmailNotificationStatus.objects.create(
            user=user, publication_date=self.publication_date
        )

    def test_str_method_return_string(self):
        '''
        `EmailNotificationStatus` model entry `__str__()` method should return the
        `publication_date`

        e.g. '28/03/2020'
        '''

        self.assertEqual(str(self.entry), '28/03/2020')

    def test_entry_status_idle_by_default(self):
        '''
        `EmailNotificationStatus` model entry `status` field should be `IDLE` by default
        '''

        self.assertEqual(self.entry.status, models.EmailNotificationStatus.IDLE)

    def test_set_status_updates_status_if_valid(self):
        '''
        `EmailNotificationStatus` model entry `set_status()` method should update the entry
        status if a valid `status` is input
        '''

        # Update the status to `EmailNotificationStatus.PROCESSING`
        self.entry.set_status(models.EmailNotificationStatus.PROCESSING)

        self.assertEqual(self.entry.status, models.EmailNotificationStatus.PROCESSING)

    def test_set_status_doesnt_update_status_if_invalid(self):
        '''
        `EmailNotificationStatus` model entry `set_status()` method should not update the entry
        status if an invalid `status` is input

        8 is an invalid status
        '''

        # Update the status to `8` which is invalid
        self.entry.set_status(8)

        # Status should remain the default `IDLE`
        self.assertEqual(self.entry.status, models.EmailNotificationStatus.IDLE)

    def test_set_status_updates_status_message(self):
        '''
        `EmailNotificationStatus` model entry `set_status()` method should update the entry
        `status_msg` if an arg is supplied
        '''

        msg_str = 'I''m processing'

        self.entry.set_status(models.EmailNotificationStatus.PROCESSING, msg_str)

        self.assertEqual(self.entry.status_msg, msg_str)

    def test_set_status_doesnt_update_status_message(self):
        '''
        `EmailNotificationStatus` model entry `set_status()` method should not update the
        entry `status_msg` if an arg is not supplied
        '''

        # No arg supplied
        self.entry.set_status(models.EmailNotificationStatus.PROCESSING)

        self.assertIsNone(self.entry.status_msg)
