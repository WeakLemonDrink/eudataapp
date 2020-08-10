'''
Tests to fix bugs found for `tenders` Django web application
'''


from django.conf import settings
from django.test import TestCase

from tenders.forms import UploadXmlFileForm
from tenders.tests.helpers import create_files_data


class ContractAwardNoticeUpload2019S147361481Tests(TestCase):
    '''
    TestCase class to help fix bugs with uploading the 2019-OJS147-361481.xml file
    '''

    fixtures = [
        './files/initial_data/countries.xml',
        './files/initial_data/currencies.xml'
    ]

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        # Need to create a related contract notice to satisfy code
        contract_notice = create_files_data('2019-OJS053-121491.xml', settings.TEST_FILES_DIR)
        contract_notice_form = UploadXmlFileForm({}, contract_notice)
        contract_notice_form.is_valid()
        contract_notice_form.save()

        # request.POST data needs to be an empty dictionary to satisfy the form structure
        upload_file = create_files_data('2019-OJS147-361481.xml', settings.TEST_FILES_DIR)
        self.form = UploadXmlFileForm({}, upload_file)

    def test_file_upload_returns_is_valid_true(self):
        '''
        2019-OJS147-361481.xml contact award notice save does not work because the
        value_of_procurement is none

        Is valid returns true
        '''

        #  Confirm `.is_valid()` method returns `True`
        self.assertTrue(self.form.is_valid())

    def test_file_upload_creates_new_contract_award_notice_successfully(self):
        '''
        2019-OJS147-361481.xml contact award notice save does not work because the
        value_of_procurement is none
        '''

        # Call is_valid first
        self.form.is_valid()

        new_tender = self.form.save()

        # New tender should be created successfully and return the correct names string
        self.assertEqual(str(new_tender), '2019/S 147-361481')


class ContractAwardNoticeUpload2019S147361501Tests(TestCase):
    '''
    TestCase class to help fix bugs with uploading the 2019-OJS147-361501.xml file
    '''

    fixtures = [
        './files/initial_data/countries.xml',
        './files/initial_data/currencies.xml'
    ]

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        # Need to create a related contract notice to satisfy code
        contract_notice = create_files_data('2019-OJS102-246675.xml', settings.TEST_FILES_DIR)
        contract_notice_form = UploadXmlFileForm({}, contract_notice)
        contract_notice_form.is_valid()
        contract_notice_form.save()

        # request.POST data needs to be an empty dictionary to satisfy the form structure
        upload_file = create_files_data('2019-OJS147-361501.xml', settings.TEST_FILES_DIR)
        self.form = UploadXmlFileForm({}, upload_file)

    def test_file_upload_returns_is_valid_true(self):
        '''
        2019-OJS147-361501.xml contract award notice save does not work because a lot value is
        coming through as `None`

        Is valid returns true
        '''

        #  Confirm `.is_valid()` method returns `True`
        self.assertTrue(self.form.is_valid())

    def test_file_upload_creates_new_tender_successfully(self):
        '''
        2019-OJS147-361501.xml contract award notice save does not work because the
        value_of_procurement is `None`
        '''

        # Call is_valid first
        self.form.is_valid()

        new_tender = self.form.save()

        # New tender should be created successfully and return the correct names string
        self.assertEqual(str(new_tender), '2019/S 147-361501')


class CountryCurrencyIsActiveTests(TestCase):
    '''
    TestCase class to help fix bug when creating new Lots

    As we are using `bulk_create` to create new `Lot` entries, the `Lot.save()` method is not
    called. This means some `Country` and `Currency` foreignkeys may not be set to
    `is_active==True`, and they won't be available in the filter

    We can add an extra call to the `Country` and `Currency` `set_is_active` methods when creating
    Lots using the `helpers.create_lots` method
    '''

    fixtures = [
        './files/initial_data/countries.xml',
        './files/initial_data/currencies.xml'
    ]

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        # request.POST data needs to be an empty dictionary to satisfy the form structure
        upload_file = create_files_data('2019-OJS093-224329.xml', settings.TEST_FILES_DIR)
        self.form = UploadXmlFileForm({}, upload_file)

    def test_all_country_foreign_keys_are_set_is_active_true(self):
        '''
        `UploadXmlFileForm` calls `helpers.create_lots` to create new Lot entries
        This should set all `Country` foreignkeys to `is_active==True` on creation
        '''

        # Call is_valid first
        self.form.is_valid()

        # use the form to create the new `tender` and associated `lots`
        new_tender = self.form.save()

        # Confirm that no associated lots have `Country` foreignkeys with `is_active==False`
        self.assertEqual(new_tender.lot_set.filter(contractor_country__is_active=False).count(), 0)

    def test_all_currency_foreign_keys_are_set_is_active_true(self):
        '''
        `UploadXmlFileForm` calls `helpers.create_lots` to create new Lot entries
        This should set all `Currency` foreignkeys to `is_active==True` on creation
        '''

        # Call is_valid first
        self.form.is_valid()

        # use the form to create the new `tender` and associated `lots`
        new_tender = self.form.save()

        # Confirm that no associated lots have `Currency` foreignkeys with `is_active==False`
        self.assertEqual(new_tender.lot_set.filter(currency__is_active=False).count(), 0)
