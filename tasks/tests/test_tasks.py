'''
Tests for tasks in the `tasks` Django web application
'''


from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from profiles.models import TedSearchTerm
from tasks import tasks
from tasks.models import EmailNotificationStatus
from tenders import models
from tenders.tests.helpers import create_contract_notice_file_data


class BulkTenderCreateTaskTests(TestCase):
    '''
    TestCase class for the `bulk_tender_create_task` task
    '''

    fixtures = [
        './files/initial_data/countries.xml',
        './files/initial_data/currencies.xml'
    ]

    def setUp(self):
        '''
        Common across individual tests
        '''

        # File is a valid TED daily export archive file
        self.filename = '20190719_2019138.tar.gz'

    def test_task_creates_contract_award_notices(self):
        '''
        `bulk_tender_create_task` method should loop through all files in `extract_dir` and
        save data to new `ContractAwardNotice`, `ContractNotice` and `Lot` entries if the
        uploaded archive is a valid TED bulk export .tar.gz

        File 20190719_2019138.tar.gz is a valid TED daily export archive file
        '''

        # Process the file
        tasks.bulk_tender_create_task(self.filename)

        # File doesn't contain any contract award notices that are linked to existing contract
        # notices in the database
        self.assertEqual(models.ContractAwardNotice.objects.all().count(), 0)

    def test_task_creates_contract_notices(self):
        '''
        `bulk_tender_create_task` method should loop through all files in `extract_dir` and
        save data to new `ContractAwardNotice`, `ContractNotice` and `Lot` entries if the
        uploaded archive is a valid TED bulk export .tar.gz

        File 20190719_2019138.tar.gz is a valid TED daily export archive file
        '''

        # Process the file
        tasks.bulk_tender_create_task(self.filename)

        # File contains 11 relevant contract notices
        self.assertEqual(models.ContractNotice.objects.all().count(), 9)


class EmailNotificationsTaskTests(TestCase):
    '''
    TestCase class for the `email_notifications_task` task
    '''

    fixtures = [
        './files/initial_data/countries.xml',
        './files/initial_data/currencies.xml'
    ]

    def setUp(self):
        '''
        Common setup
        '''

        self.user = User.objects.create(
            username='jblogs', email='joseph.blogs@django.com', password='jblogspassword',
            first_name='Joseph'
        )

    def test_task_returns_str_if_no_search_terms_exist(self):
        '''
        `email_notifications_task` should do nothing and return a status string if no
        `TedSearchTerm` entries associated with the input user exist
        '''

        return_str = tasks.email_notifications_task(self.user.id)

        self.assertEqual(return_str, 'No TedSearchTerm entries associated with user account.')

    def test_task_returns_str_if_email_status_exists(self):
        '''
        `email_notifications_task` should do nothing and return a status string if `TedSearchTerm`
        entries associated with the input user exist but a `EmailNotificationStatus` entry already
        exists for the user and date

        This indicates an email has already been sent
        '''

        # Create a search term and email status
        TedSearchTerm.objects.create(user=self.user, keyword='searchterm')
        EmailNotificationStatus.objects.create(
            user=self.user, status=EmailNotificationStatus.COMPLETE,
            publication_date=timezone.now()
        )

        return_str = tasks.email_notifications_task(self.user.id)

        self.assertEqual(
            return_str,
            'Notifications already processed for ' + timezone.now().strftime('%d/%m/%Y.')
        )

    def test_task_creates_email_status_entry(self):
        '''
        `email_notifications_task` should create a new `EmailNotificationStatus` entry associated
        with the user if `TedSearchTerm` entries associated with the input user exist but an
        existing `EmailNotificationStatus` entry for the date doesn't exist
        '''

        # Create a search term
        TedSearchTerm.objects.create(user=self.user, keyword='searchterm')

        tasks.email_notifications_task(self.user.id)

        # Confirm a new `EmailNotificationStatus` entry has been created associated with the user
        self.assertTrue(EmailNotificationStatus.objects.filter(user=self.user).exists())

    def test_task_returns_no_matches_str(self):
        '''
        `email_notifications_task` should return a no matches string if notifications have not
        already been processed, but no matches to the search terms in `ContractNotice` entries
        are found
        '''

        # Create a search term
        TedSearchTerm.objects.create(user=self.user, keyword='searchterm')

        return_str = tasks.email_notifications_task(self.user.id)

        # Confirm return string that should be the same as the new `EmailNotificationStatus`
        # entry status_msg field
        self.assertEqual(return_str, 'No matches found.')

    def test_task_sends_mail(self):
        '''
        `email_notifications_task` should send an email to the user stating that matches have
        been found if they have been found!
        '''

        # Create a search term, contract notice and lot
        TedSearchTerm.objects.create(user=self.user, keyword='searchterm')

        cn_data = create_contract_notice_file_data()
        # Update the `publication_date` to today
        cn_data['publication_date'] = timezone.now()

        c_n = models.ContractNotice.objects.create(**cn_data)
        models.Lot.objects.create(contract_notice=c_n, lot_no=1, title='My searchterm lot',
                                  search_vector='My searchterm lot')

        tasks.email_notifications_task(self.user.id)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)


class EmailUserNotificationsTaskTests(TestCase):
    '''
    TestCase class for the `email_user_notifications_task` task
    '''

    fixtures = [
        './files/initial_data/countries.xml',
        './files/initial_data/currencies.xml'
    ]

    def test_email_user_notifications_task_if_no_contract_notices(self):
        '''
        `email_user_notifications_task` should not do anything and just return a string if no
        ContractNotice entries for today's date exist

        Test just to confirm a return string is returned without error
        '''

        return_str = tasks.email_user_notifications_task()

        self.assertTrue(return_str)

    def test_email_user_notifications_task_if_contract_notices_exist(self):
        '''
        `email_user_notifications_task` should not do anything and just return a string if no
        ContractNotice entries for today's date exist

        Test just to confirm a return string is returned without error
        '''

        # Create some contract notices with today's date
        cn_data = create_contract_notice_file_data()
        # Update the `publication_date` to today
        cn_data['publication_date'] = timezone.now()

        c_n = models.ContractNotice.objects.create(**cn_data)

        return_str = tasks.email_user_notifications_task()

        self.assertTrue(return_str)


class GetDailyPackageTaskTests(TestCase):
    '''
    TestCase class for the `get_daily_package_task` task
    '''

    fixtures = [
        './files/initial_data/countries.xml',
        './files/initial_data/currencies.xml'
    ]

    def test_task_creates_contract_award_notices(self):
        '''
        `get_daily_package_task` method try and retrieve a valid ftp file for an input date

        09/10/2019 should have a valid daily export archive file on the ftp server
        '''

        # Process the file
        tasks.get_daily_package_task('09/10/2019')

        # File doesn't contain any contract award notices that are linked to existing contract
        # notices in the database
        self.assertEqual(models.ContractAwardNotice.objects.all().count(), 0)

    def test_task_creates_contract_notices(self):
        '''
        `get_daily_package_task` method try and retrieve a valid ftp file for an input date

        09/10/2019 should have a valid daily export archive file on the ftp server
        '''

        # Process the file
        tasks.get_daily_package_task('09/10/2019')

        # File cotains 7 relevant cotract notices
        self.assertEqual(models.ContractNotice.objects.all().count(), 3)

    def test_task_is_valid_return_str(self):
        '''
        `get_daily_package_task` method try and retrieve a valid ftp file for an input date

        09/10/2019 should have a valid daily export archive file on the ftp server and should
        return a success string
        '''

        date_str = '09/10/2019'

        # Process the file
        return_str = tasks.get_daily_package_task(date_str)

        self.assertEqual(
            return_str,
            'Complete: ' + date_str + ' 0 new Contract Award Notice(s) and 3 new Contract ' + \
            'Notice(s) added to the database successfully.'
        )

    def test_date_is_not_valid_error_str(self):
        '''
        `get_daily_package_task` method try and retrieve a valid ftp file for an input date

        13/10/2019 should not have a valid daily export archive file on the ftp server. It should
        return an error string for debug purposes
        '''

        date_str = '13/10/2019'

        # Process the file
        return_str = tasks.get_daily_package_task(date_str)

        self.assertEqual(
            return_str,
            date_str + ' Daily package for this date is not available on the ftp server.'
        )

    def test_no_date_supplied_as_input(self):
        '''
        `get_daily_package_task` called without an input should use todays date to find a package
        on the ftp server
        '''

        return_str = tasks.get_daily_package_task()

        todays_date = timezone.now()

        # Check that todays_date is in the return string. This will confirm todays date has been
        # used
        self.assertTrue(todays_date.strftime('%d/%m/%Y') in return_str)
