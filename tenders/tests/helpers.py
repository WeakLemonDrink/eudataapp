'''
Helpers for tests in the `tenders` Django web application
'''


import datetime
import os
import sys
import pytz

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import Client

from tenders import models


def create_files_data(file_name, file_path=None):
    '''
    Method creates files data to test uploads to forms

     * If `file_path` is `None`, just creates a dummy file with `file_name` and attaches it
       to files dictionary
     * If `file_path` is not `None`, opens the file and attaches it to files dictionary
    '''

    if file_path:
        upload_file = open(os.path.join(file_path, file_name), 'rb')

        upload_file_name = upload_file.name
        upload_file_read = upload_file.read()

    else:
        upload_file_name = file_name
        upload_file_read = bytes(2)

    return {'upload_file': SimpleUploadedFile(upload_file_name, upload_file_read)}


def create_contract_award_notice_file_data():
    '''
    Method returns data to create a `ContractAwardNotice` entry using data from a valid TED export
    file

    Entry data taken from ./files/test/2019-OJS072-170256.xml
    '''

    entry_data = {
        'contracting_body_name': 'Uniwersytecki Szpital Dziecięcy w Lublinie',
        'country': models.Country.objects.get(iso_code='HU'),
        'currency': models.Currency.objects.get(iso_code='HUF'),
        'dispatch_date': datetime.date(2019, 4, 9),
        'ojs_ref': '2019/S 072-170256',
        'publication_date': datetime.date(2019, 4, 11),
        'short_descr': [
            'Gyógyszerek és egyéb termékek beszerzése a Borsod-Abaúj-Zemplén Megyei Központi ' +
            'Kórház és Egyetemi Oktatókórházra részére 12+12 hónapos időtartamra.'
        ],
        'title': 'Postępowanie o udzielenie zamówienia publicznego w trybie przetargu ' +
                 'nieograniczonego na dostawy leków',
        'url': 'http://ted.europa.eu/udl?uri=TED:NOTICE:170256-2019:TEXT:HU:HTML',
        'value_of_procurement': 387977728,
    }

    return entry_data


def create_contract_notice_file_data():
    '''
    Method returns data to create a `ContractNotice` entry using data from a valid TED export file

    Entry data taken from ./files/test/2018-OJS191-431371.xml, linked to 2019-OJS072-170256.xml
    contract award notice data used in `create_contract_award_notice_file_data`
    '''

    entry_data = {
        'contracting_body_name': 'Borsod-Abaúj-Zemplén Megyei Központi Kórház és Egyetemi ' +
                                 'Oktatókórház',
        'country': models.Country.objects.get(iso_code='HU'),
        'closing_date': datetime.datetime(
            2018, 11, 5, 13, 00, tzinfo=pytz.timezone('Europe/Brussels')
        ),
        'dispatch_date': datetime.date(2018, 10, 2),
        'ojs_ref': '2018/S 191-431371',
        'publication_date': datetime.date(2018, 10, 4),
        'short_descr': [
            'Gyógyszerek és egyéb termékek beszerzése a Borsod-Abaúj-Zemplén Megyei Központi ' +
            'Kórház és Egyetemi Oktatókórházra részére 12+12 hónapos időtartamra.'
        ],
        'title': 'Gyógyszerek, egyéb termékek beszerzése BAZ Kórház',
        'url': 'http://ted.europa.eu/udl?uri=TED:NOTICE:431371-2018:TEXT:HU:HTML',
        'procurement_ref': 'EKR000644792018',
        'procurement_docs_url': 'https://ekr.gov.hu/portal/kozbeszerzes/eljarasok/' +
                                'EKR000644792018/reszletek',
        'full_docs_available': True
    }

    return entry_data


def dump_to_fixtures(args):
    '''
    Method dumps data to a fixture
    '''

    sysout = sys.stdout
    sys.stdout = open('fixture.xml', 'w')
    call_command('dumpdata', *args, indent=4, format='xml')
    sys.stdout = sysout


def load_fixtures(test_case, fixture_name):
    '''
    Method loads fixtures if they exist for a test based on its `test_case` attributes and
    `test_name`
    '''

    # Build the expected file path from `test_case` attributes
    fixture_path = os.path.join(
        settings.TEST_FILES_DIR, 'fixtures', *test_case.__module__.split('.'),
        test_case.__class__.__name__, fixture_name
    )

    # If file exists, load the fixutre
    if os.path.isfile(fixture_path):
        call_command('loaddata', fixture_path, verbosity=0)


def view_test_setup(test_case):
    '''
    Method creates common test data attached to the input `test_case` instance for use across
    tests
    '''

    test_case.client = Client()
    test_case.user = User.objects.create_user('jblogs', 'joseph.blogs@django.com',
                                              'jblogspassword')
