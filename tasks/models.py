'''
Models for the `tasks` Django app
'''


import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DailyPackageDownloadStatus(models.Model):
    '''
    Defines database table structure for `DailyPackageDownloadStatus` entries

    Monitors status when bulk uploading a TED file
    '''

    IDLE = 0
    DOWNLOADING = 1
    PROCESSING = 2
    ERROR = 3
    TIMEOUT = 4
    COMPLETE = 5

    STATUS_CHOICES = [
        (IDLE, 'Idle'),
        (DOWNLOADING, 'Downloading'),
        (PROCESSING, 'Processing'),
        (ERROR, 'Error'),
        (TIMEOUT, 'Timeout'),
        (COMPLETE, 'Complete'),
    ]

    added = models.DateTimeField('Added Timestamp', auto_now_add=True)
    modified = models.DateTimeField('Modified Timestamp', auto_now=True)
    file_name = models.CharField('File Name', max_length=140, unique=True)
    file_date = models.DateTimeField('File Date')
    status = models.PositiveIntegerField('Status', choices=STATUS_CHOICES, default=IDLE)
    status_msg = models.CharField('Status Message', max_length=400, null=True, blank=True)

    class Meta:
        app_label = 'tasks'
        ordering = ['-file_date']
        verbose_name = 'Daily Package Download Status'
        verbose_name_plural = 'Daily Package Download Statuses'

    def is_error(self):
        '''
        Returns `True` if `self.status` is an error, otherwise `False`
        '''

        return self.status == self.ERROR

    def save(self, *args, **kwargs):
        '''
        Override save method to populate `file_date` on initial save

        This should be grabbed from the date string in the `file_name` e.g. 20190801_2019147.tar.gz
        '''

        if self.pk is None:
            self.file_date = timezone.make_aware(
                datetime.datetime.strptime(self.file_name[:8], '%Y%m%d')
            )

        # Call default save
        super().save(*args, **kwargs)

    def set_status(self, status, *args):
        '''
        Sets the `status` field if a member of `STATUS_CHOICES` and saves the entry

        Also sets `status_msg` if a message string is supplied
        '''

        if status in [i for i, _ in self.STATUS_CHOICES]:
            self.status = status

            if args:
                self.status_msg = args[0]

            self.save()

    def __str__(self):
        '''
        Defines the return string for a `DailyPackageDownloadStatus` entry
        '''

        return self.file_name


class EmailNotificationStatus(models.Model):
    '''
    Defines database table structure for `EmailNotificationStatus` entries

    Monitors status when sending notifications emails to users
    '''

    IDLE = 0
    PROCESSING = 1
    ERROR = 2
    COMPLETE = 3

    STATUS_CHOICES = [
        (IDLE, 'Idle'),
        (PROCESSING, 'Processing'),
        (ERROR, 'Error'),
        (COMPLETE, 'Complete'),
    ]

    added = models.DateTimeField('Added Timestamp', auto_now_add=True)
    modified = models.DateTimeField('Modified Timestamp', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateField('Publication Date')
    status = models.PositiveIntegerField('Status', choices=STATUS_CHOICES, default=IDLE)
    status_msg = models.CharField('Status Message', max_length=400, null=True, blank=True)

    class Meta:
        app_label = 'tasks'
        ordering = ['-publication_date']
        verbose_name = 'Email Notification Status'
        verbose_name_plural = 'Email Notification Statuses'

    def set_status(self, status, *args):
        '''
        Sets the `status` field if a member of `STATUS_CHOICES` and saves the entry

        Also sets `status_msg` if a message string is supplied
        '''

        if status in [i for i, _ in self.STATUS_CHOICES]:
            self.status = status

            if args:
                self.status_msg = args[0]

            self.save()

    def __str__(self):
        '''
        Defines the return string for a `EmailNotificationStatus` entry
        '''

        return datetime.datetime.strftime(self.publication_date, '%d/%m/%Y')
