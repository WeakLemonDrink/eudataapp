'''
Models for the `profiles` Django app
'''

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class TedSearchTerm(models.Model):
    '''
    Defines database table structure for `TedSearchTerm` entries
    '''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^[\S]*$',
                message='Keyword is not a single word.'
            )
        ]
    )
    send_notifications = models.BooleanField(
        'Send Notifications', default=True,
        help_text='Send email notifications when search term matches a Contract Notice'
    )
    is_active = models.BooleanField(
        'Is Active', default=True,
        help_text='Use search term to find matching Contract Notices'
    )

    class Meta:
        app_label = 'profiles'
        ordering = ['keyword']
        unique_together = ['user', 'keyword']
        verbose_name = 'TED Search Term'

    def save(self, *args, **kwargs):
        '''
        Override default save to set input `keyword` to lower case
        '''

        self.keyword = self.keyword.lower()

        # Call default save
        super().save(*args, **kwargs)

    def __str__(self):
        '''
        Defines the return string for a `TedSearchTerm` entry
        '''

        return self.keyword
