'''
Celery tasks for `tenders` Django web app.
'''


from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from django.utils import timezone
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

from profiles.models import TedSearchTerm
from profiles.helpers import get_search_term_matches
from tasks import helpers
from tasks.models import DailyPackageDownloadStatus, EmailNotificationStatus
from tenders.forms import DailyPackageDownloadForm
from tenders import models


@shared_task(soft_time_limit=25, time_limit=28)
def bulk_tender_create_task(file_name):
    '''
    Task to call `bulk_tender_create` method to create new `tenders` and `lots` from file at
    `file_name`
    '''

    task_status, _ = DailyPackageDownloadStatus.objects.get_or_create(file_name=file_name)

    try:
        helpers.bulk_tender_create(task_status)

    except SoftTimeLimitExceeded:
        # Delete all the temporary files and record that the task timed out
        helpers.clear_temp_files_dir()

        task_status.set_status(
            DailyPackageDownloadStatus.TIMEOUT, 'bulk_tender_create_task timeout.'
        )

    return '{}: {}'.format(task_status.get_status_display(), task_status.status_msg)


@shared_task
def email_notifications_task(user_id):
    '''
    Task to email user defined by input `user_id` if any of their `TedSearchTerm` entries match a
    search over a queryset of `ContractNotice` entries
    '''

    user = User.objects.get(id=user_id)
    search_term_qs = TedSearchTerm.objects.filter(user=user, send_notifications=True,
                                                  is_active=True)

    publication_date = timezone.now()

    # Has the user got any `TedSearchTerm` entries associated with their account?
    if search_term_qs.exists():
        # Has a successful email notification already been sent today?
        email_status, _ = EmailNotificationStatus.objects.get_or_create(
            user=user, publication_date=publication_date
        )

        if not email_status.status == EmailNotificationStatus.COMPLETE:
            # Not complete so search through `ContractNotice` entries with publication_date
            email_status.set_status(EmailNotificationStatus.PROCESSING)

            cn_qs = models.ContractNotice.objects.filter(publication_date=publication_date)

            # Search for any matches and email a notification if any are found
            if get_search_term_matches(search_term_qs, cn_qs):
                mail_sent = send_mail(
                    'Tedsearch found matches for your search terms!',
                    'Hi ' + user.first_name + ',\n\r' + \
                    'Contract Notices uploaded to the Tedsearch web application today match ' + \
                    'one or more of your search terms.\n\r' + \
                    'View matching Contract Notices on your dashboard at '+ \
                    '{}{}?publication_date={:%d/%m/%Y}\n\r'.format(
                        settings.BASE_URL, reverse('profiles:dashboard'), publication_date
                    ) + \
                    'All the best,\n\r' + \
                    'Tedsearch',
                    settings.EMAIL_FROM_ADDR,
                    [user.email]
                )

                if mail_sent == 1:
                    # Indicates mail was sent successfully
                    email_status.set_status(
                        EmailNotificationStatus.COMPLETE, 'Matches found. Email sent successfully.'
                    )

                else:
                    # Indicates error
                    email_status.set_status(
                        EmailNotificationStatus.ERROR, 'Matches found. Email not sent.'
                    )

            else:
                # No matches found
                email_status.set_status(
                    EmailNotificationStatus.COMPLETE, 'No matches found.'
                )

            # Set the return string to the status_msg
            return_str = email_status.status_msg

        else:
            return_str = 'Notifications already processed for ' + \
                         publication_date.strftime('%d/%m/%Y.')

    else:
        return_str = 'No TedSearchTerm entries associated with user account.'

    return return_str


@shared_task(soft_time_limit=25, time_limit=28)
def email_user_notifications_task():
    '''
    Task to search through new `ContractNotice` entries and email users if any `ContractNotice`
    entries match their search terms
    '''

    publication_date = timezone.now()

    # Check a valid `ContractNotice` queryset exists
    if models.ContractNotice.objects.filter(publication_date=publication_date).exists():
        # Loop through all active users and call subtask to send emails
        for user in User.objects.exclude(email=None, first_name=None, is_active=False):
            email_notifications_task.delay(user.id)

        return_str = 'email_notifications_task subtask called succesfully.'

    else:
        return_str = 'No Contract Notices with publication date ' + \
                     '{:%d/%m/%Y} exist. Notifications  not sent.'.format(publication_date)

    return return_str


@shared_task
def get_daily_package_task(date=None):
    '''
    Task to get daily package .tar.gz file from the ftp server for the input `date`

    `date` should be a string in the format '%d/%m/%Y'. If no data is supplied, use todays date
    `date` is retained as an input here for use with testing.
    '''

    # If no date supplied, use todays date
    if not date:
        date = timezone.now().strftime('%d/%m/%Y')

    # Use `DailyPackageDownloadForm` to check a valid file exists for this date
    form = DailyPackageDownloadForm({'date': date})

    # If date has a good file on the ftp, download and process it
    if form.is_valid():
        # Create a new `DailyPackageDownloadStatus` entry to track processing progress
        task_status, _ = DailyPackageDownloadStatus.objects.get_or_create(file_name=form.file_name)

        # Call `bulk_tender_create` and timeout if it takes too long
        try:
            helpers.bulk_tender_create(task_status)

        except SoftTimeLimitExceeded:
            # Delete all the temporary files and record that the task timed out
            helpers.clear_temp_files_dir()

            task_status.set_status(
                DailyPackageDownloadStatus.TIMEOUT, 'get_daily_package_task timeout.'
            )

        return_str = '{}: {:%d/%m/%Y} {}'.format(
            task_status.get_status_display(), task_status.file_date, task_status.status_msg
        )

    else:
        # If the form isn't valid, return the errors as a return string
        return_str = date + ' ' + ', '.join(form.errors['date'])

    return return_str


@shared_task
def update_lot_search_vector():
    '''
    Task to perform update on `Lot` database table to do populate the `search_vector` column with
    the correct data using triggers
    '''

    models.Lot.objects.update(search_vector=SearchVector('title', 'short_descr', 'info_add'))

    return 'Lot search vector updated.'
