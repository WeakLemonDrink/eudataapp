'''
Tests for `tenders.models` in the `tenders` Django web application
'''


import datetime
import os

from botocore import exceptions
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from tenders import models
from tenders.helpers import new_s3_client
from tenders.tests import helpers


class UpdateUrlLanguageTabTests(TestCase):
    '''
    TestCase class for the `update_url_language_tab` helper function
    '''

    def test_url_language_tab_is_updated_match(self):
        '''
        Returns an updated url replacing the language tab (e.g. 'PL') with 'EN' if it exists. This
        ensures the page at the given url will be in English when clicked

        If the regex matches, `url` is updated with 'EN' language tab and returned as `return_url`
        '''

        input_url = 'http://ted.europa.eu/udl?uri=TED:NOTICE:384676-2019:TEXT:PL:HTML'

        updated_url = 'http://ted.europa.eu/udl?uri=TED:NOTICE:384676-2019:TEXT:EN:HTML'

        self.assertEqual(updated_url, models.update_url_language_tab(input_url))

    def test_url_language_tab_is_not_updated_no_match(self):
        '''
        Returns an updated url replacing the language tab (e.g. 'PL') with 'EN' if it exists. This
        ensures the page at the given url will be in English when clicked

        If the regex doesn't match, `url` is returned unmodified
        '''

        input_url = 'www.zoz-debica.pl'

        self.assertEqual(input_url, models.update_url_language_tab(input_url))


class CountryModelTests(TestCase):
    '''
    TestCase class for the `Country` model
    '''

    fixtures = ['./files/initial_data/countries.xml', ]

    def setUp(self):
        '''
        Common setup for each test
        '''

        self.entry = models.Country.objects.get(iso_code='GB')

    def test_str_method_return_string(self):
        '''
        `Country` model entry `__str__()` method should return the `iso_code` and `country_name`

        e.g. 'GB United Kingdom of Great Britain and Northern Ireland'
        '''

        self.assertEqual(
            str(self.entry), '{} {}'.format(self.entry.iso_code, self.entry.country_name)
        )

    def test_is_active_is_false_by_default(self):
        '''
        `Country` model entries should be `is_active=False` by default
        '''

        self.assertFalse(self.entry.is_active)

    def test_set_is_active_method_if_is_active_false(self):
        '''
        `Country` model entry `set_is_active()` method sould set `is_active` to `True` and save if
        `is_active` is `False`

        self.entry has `is_active=False` by default
        '''

        # Call `set_is_active()` method to set `is_active` to `True`
        self.entry.set_is_active()

        # Confirm `is_active` is `True`
        self.assertTrue(self.entry.is_active)

    def test_set_is_active_method_if_is_active_true(self):
        '''
        `Country` model entry `set_is_active()` method sould not modify `is_active` if `is_active`
        is `True`

        self.entry has `is_active=False` by default
        '''

        # Manually set `is_active` to `True` and save
        self.entry.is_active = True
        self.entry.save()

        # Call `set_is_active()` method to set `is_active` to `True`
        self.entry.set_is_active()

        # Confirm `is_active` is still `True`
        self.assertTrue(self.entry.is_active)


class CurrencyModelTests(TestCase):
    '''
    TestCase class for the `Currency` model
    '''

    fixtures = ['./files/initial_data/currencies.xml', ]

    def setUp(self):
        '''
        Common setup for each test
        '''

        self.entry = models.Currency.objects.get(iso_code='EUR')

    def test_str_method_return_string(self):
        '''
        `Currency` model entry `__str__()` method should return the `iso_code` and `currency_name`

        e.g. 'EUR Euro'
        '''

        self.assertEqual(
            str(self.entry), '{} {}'.format(self.entry.iso_code, self.entry.currency_name)
        )

    def test_is_active_is_false_by_default(self):
        '''
        `Currency` model entries should be `is_active=False` by default
        '''

        self.assertFalse(self.entry.is_active)

    def test_set_is_active_method_if_is_active_false(self):
        '''
        `Country` model entry `set_is_active()` method sould set `is_active` to `True` and save if
        `is_active` is `False`

        self.entry has `is_active=False` by default
        '''

        # Call `set_is_active()` method to set `is_active` to `True`
        self.entry.set_is_active()

        # Confirm `is_active` is `True`
        self.assertTrue(self.entry.is_active)

    def test_set_is_active_method_if_is_active_true(self):
        '''
        `Country` model entry `set_is_active()` method sould not modify `is_active` if `is_active`
        is `True`

        self.entry has `is_active=False` by default
        '''

        # Manually set `is_active` to `True` and save
        self.entry.is_active = True
        self.entry.save()

        # Call `set_is_active()` method to set `is_active` to `True`
        self.entry.set_is_active()

        # Confirm `is_active` is still `True`
        self.assertTrue(self.entry.is_active)


class ContractNoticeModelTests(TestCase):
    '''
    TestCase class for the `ContractNotice` model
    '''

    fixtures = [
        './files/initial_data/countries.xml'
    ]

    def setUp(self):
        '''
        Common setup for each test
        '''

        # Entry data taken from ./files/test/2019-OJS156-384676.xml
        self.entry_data = helpers.create_contract_notice_file_data()
        self.entry = models.ContractNotice.objects.create(**self.entry_data)

    def test_str_method_return_string(self):
        '''
        `ContractNotice` model entry `__str__()` method should return the `ojs_ref`, which is a
        unique identifier for a TED contract notice
        '''

        self.assertEqual(str(self.entry), self.entry.ojs_ref)

    def test_save_method_modifies_url(self):
        '''
        `ContractNotice` model entry `save()` method should modify the `url` string on save to
        make sure it has the 'EN' language tag

        Urls in the TED export have the tender native language in the url string. We need to
        change this to 'EN' to make sure the page is readable when we click on the link
        '''

        # original url is 'HU', this should be changed to 'EN'                   ^^
        expected_url = 'http://ted.europa.eu/udl?uri=TED:NOTICE:431371-2018:TEXT:EN:HTML'

        self.assertEqual(self.entry.url, expected_url)

    def test_save_method_updates_country_is_active(self):
        '''
        `ContractNotice` model entry `save()` method should call `country.set_is_active()` method
        to set `country.is_active` to `True`

        This will allow us to filter `Country` entries more effectively when `ContractNotice`
        entries are in a table
        '''

        # `Create` method will have called `entry.save()` method already
        self.assertTrue(self.entry.country.is_active)

    def test_save_method_short_descr_concatenates_list_if_present(self):
        '''
        `ContractNotice` model entry `save()` method should concatenate a list of strings with
        newlines and save to `short_descr` if a list is provided to the field on save
        '''

        # Update the data to include a list of strings in the `short_descr`
        str_list = ['my', 'short', 'description', 'string', 'list']

        self.entry_data['short_descr'] = str_list
        # Update the `ojs_ref` in the entry_data to make sure it doesn't clash with `self.entry`
        self.entry_data['ojs_ref'] = 'my baljs'

        # Create the entry with this updated data
        entry = models.ContractNotice.objects.create(**self.entry_data)

        self.assertEqual(entry.short_descr, '\n'.join(str_list))

    def test_contract_notice_file_saves_file_in_correct_location(self):
        '''
        `ContractNotice` model entry `procurement_docs_file` field should save any uploaded file to
        a location based on the model name and id on AWS S3

        `procurement_docs_file` upload should only be done to an existing contract notice, not as
        part of a new entry creation

        location should be MEDIA_ROOT/<app_label>/<model_name>/<id>/<filename> e.g.
                           MEDIA_ROOT/tenders/contractnotice/1/myfile.xlsx
        '''

        # Update the data to include a file
        file_name = 'myfile.xlsx'
        file_key = os.path.join(
            settings.MEDIA_LOCATION, self.entry._meta.app_label, self.entry._meta.model_name,
            str(self.entry.id), file_name
        )

        self.entry.procurement_docs_file = SimpleUploadedFile(file_name, bytes(2))

        # Save the entry with this procurement_docs_file
        self.entry.save()

        self.assertEqual(self.entry.procurement_docs_file.url,
                         os.path.join('https://%s' % settings.AWS_S3_CUSTOM_DOMAIN, file_key))

        # Delete the file from S3
        s3_client = new_s3_client()
        s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)

    def test_pre_save_signal_deletes_contract_notice_file_if_changed(self):
        '''
        `ContractNotice` model entry pre save signal `auto_delete_contract_notice_file_on_change`
        should delete an old `procurement_docs_file` from S3 if the file is changed.

        If `procurement_docs_file` is updated to `None` (i.e. deleted), the pre_save signal should
        also delete the file from S3
        '''

        # Update the data to include a file
        file_name = 'myfile.xlsx'
        file_key = os.path.join(
            settings.MEDIA_LOCATION, self.entry._meta.app_label, self.entry._meta.model_name,
            str(self.entry.id), file_name
        )

        self.entry.procurement_docs_file = SimpleUploadedFile(file_name, bytes(2))

        # Save the entry with this procurement_docs_file
        self.entry.save()

        # Update the `procurement_docs_file` to clear it
        self.entry.procurement_docs_file = None
        self.entry.save()

        # Try to delete the file. Hopefully it doesn't exist because the pre_save signal has
        # deleted it already
        s3_client = new_s3_client()
        # Should return `NoSuchKey` as key should not exist
        try:
            s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)
            obj_exists = True
        except exceptions.ClientError:
            obj_exists = False

        self.assertFalse(obj_exists)

    def test_save_method_adds_http_to_procurement_docs_url_if_required(self):
        '''
        `ContractNotice` model entry `save()` method should prepend `procurement_docs_url` with
        "http://" if its not already included in the string. This ensures the url is not treated as
        a relative url in the app
        '''

        procurement_docs_url = 'www.myprocurementdocs.com'

        # Update the entry data to make sure the url doesn't start with http
        self.entry_data['procurement_docs_url'] = 'www.myprocurementdocs.com'
        # Update the `ojs_ref` in the entry_data to make sure it doesn't clash with `self.entry`
        self.entry_data['ojs_ref'] = 'my baljs'

        # Create the entry with this updated data
        entry = models.ContractNotice.objects.create(**self.entry_data)

        self.assertEqual(entry.procurement_docs_url, 'http://' + procurement_docs_url)


class ContractAwardNoticeModelTests(TestCase):
    '''
    TestCase class for the `ContractAwardNotice` model
    '''

    fixtures = [
        './files/initial_data/countries.xml',
        './files/initial_data/currencies.xml'
    ]

    def setUp(self):
        '''
        Common setup for each test
        '''

        # Create related contract notice
        self.contract_notice = models.ContractNotice.objects.create(
            **helpers.create_contract_notice_file_data()
        )

        # Entry data taken from ./files/test/2019-OJS072-170256.xml
        self.entry_data = helpers.create_contract_award_notice_file_data()
        self.entry = models.ContractAwardNotice.objects.create(
            contract_notice=self.contract_notice, **self.entry_data
        )

    def test_str_method_return_string(self):
        '''
        `ContactAwardNotice` model entry `__str__()` method should return the `ojs_ref`, which is a
        unique identifier for a TED tender
        '''

        self.assertEqual(str(self.entry), self.entry.ojs_ref)

    def test_save_method_modifies_url(self):
        '''
        `ContactAwardNotice` model entry `save()` method should modify the `url` string on save to
        make sure it has the 'EN' language tag

        Urls in the TED export have the tender native language in the url string. We need to
        change this to 'EN' to make sure the page is readable when we click on the link
        '''

        # original url is 'HU', this should be changed to 'EN'                   ^^
        expected_url = 'http://ted.europa.eu/udl?uri=TED:NOTICE:170256-2019:TEXT:EN:HTML'

        self.assertEqual(self.entry.url, expected_url)

    def test_save_method_updates_country_is_active(self):
        '''
        `ContactAwardNotice` model entry `save()` method should call `country.set_is_active()`
        method to set `country.is_active` to `True`

        This will allow us to filter `Country` entries more effectively when `ContactNotice`
        entries are in a table
        '''

        # `Create` method will have called `entry.save()` method already
        self.assertTrue(self.entry.country.is_active)

    def test_save_method_updates_currency_is_active(self):
        '''
        `ContactAwardNotice` model entry `save()` method should call `currency.set_is_active()`
        method to set `currency.is_active` to `True`

        This will allow us to filter `Currency` entries more effectively when `ContactNotice`
        entries are in a table
        '''

        # `Create` method will have called `entry.save()` method already
        self.assertTrue(self.entry.currency.is_active)

    def test_save_method_short_descr_concatenates_list_if_present(self):
        '''
        `ContactAwardNotice` model entry `save()` method should concatenate a list of strings
        with newlines and save to `short_descr` if a list is provided to the field on save
        '''

        # Update the data to include a list of strings in the `short_descr`
        str_list = ['my', 'short', 'description', 'string', 'list']

        self.entry_data['short_descr'] = str_list
        # Update the `ojs_ref` in the entry_data to make sure it doesn't clash with `self.entry`
        self.entry_data['ojs_ref'] = 'my baljs'

        # Create the entry with this updated data
        entry = models.ContractAwardNotice.objects.create(contract_notice=self.contract_notice,
                                                          **self.entry_data)

        self.assertEqual(entry.short_descr, '\n'.join(str_list))


class LotModelTests(TestCase):
    '''
    TestCase class for the `Lot` model
    '''

    fixtures = [
        './files/initial_data/countries.xml',
        './files/initial_data/currencies.xml'
    ]

    def setUp(self):
        '''
        Common setup for each test
        '''

        # Create a test `ContractAwardNotice` and `Lot`
        tender_data = helpers.create_contract_notice_file_data()
        contract_notice = models.ContractNotice.objects.create(**tender_data)

        # Entry data taken from ./files/test/2019-OJS097-234223.xml, lot 138
        self.lot_data = {
            'lot_no': 138, 'awarded_contract': True, 'title': 'Cidofovir inj 0,375g/5ml x 1 fiol',
            'conclusion_date': datetime.date(2019, 3, 26),
            'contractor_name': 'Profarm PS Sp. z o. o.',
            'contract_notice': contract_notice,
            'contractor_country': models.Country.objects.get(iso_code='PL'),
            'value': 75750.00, 'currency': models.Currency.objects.get(iso_code='PLN'),
            'short_descr': 'Cidofovir inj 0,375g/5ml x 1 fiol 15'
        }

        # Default entry we can use for most tests
        self.entry = models.Lot.objects.create(**self.lot_data)

    def test_str_method_return_correct_string(self):
        '''
        `Lot` model entry `__str__()` method should return the `contract_notice` and `lot_no`,
        which together form a unique identifier for a TED tender lot
        '''

        self.assertEqual(
            str(self.entry),
            '{!s} Lot {!s}'.format(self.entry.contract_notice, self.entry.lot_no)
        )

    def test_save_method_updates_country_is_active(self):
        '''
        `Lot` model entry `save()` method should call `contractor_country.set_is_active()` method
        to set `contractor_country.is_active` to `True`

        This will allow us to filter `Country` entries more effectively when `Lot` entries are
        in a table
        '''

        # `Create` method will have called `entry.save()` method already
        self.assertTrue(self.entry.contractor_country.is_active)

    def test_save_method_updates_currency_is_active(self):
        '''
        `Lot` model entry `save()` method should call `currency.set_is_active()` method to
        set `currency.is_active` to `True`

        This will allow us to filter `Currency` entries more effectively when `Lot` entries are
        in a table
        '''

        # `Create` method will have called `entry.save()` method already
        self.assertTrue(self.entry.currency.is_active)

    def test_save_method_info_add_concatenates_list_if_present(self):
        '''
        `Lot` model entry `save()` method should concatenate a list of strings with newlines and
        save to `info_add` if a list is provided to the field on save
        '''

        # Update the data to include a list of strings in the `short_descr`
        str_list = ['my', 'short', 'description', 'string', 'list']

        self.lot_data['info_add'] = str_list

        # Create the entry with this updated data
        entry = models.Lot.objects.create(**self.lot_data)

        self.assertEqual(entry.info_add, '\n'.join(str_list))

    def test_save_method_short_descr_concatenates_list_if_present(self):
        '''
        `Lot` model entry `save()` method should concatenate a list of strings with newlines and
        save to `short_descr` if a list is provided to the field on save
        '''

        # Update the data to include a list of strings in the `short_descr`
        str_list = ['my', 'short', 'description', 'string', 'list']

        self.lot_data['short_descr'] = str_list

        # Create the entry with this updated data
        entry = models.Lot.objects.create(**self.lot_data)

        self.assertEqual(entry.short_descr, '\n'.join(str_list))

    def test_save_method_calculates_value_per_unit(self):
        '''
        `Lot` model entry `save()` method should calculate and fill `value_per_unit` field if data
        is available

        If `value` and `number_of_units` are filled:
           `value_per_unit` = `value` / `number_of_units`
        '''

        # Update the data to include `number_of_units`
        self.lot_data['number_of_units'] = 120

        # Create the entry with this updated data
        entry = models.Lot.objects.create(**self.lot_data)

        # `value_per_unit` should be 75750.00 / 120
        self.assertEqual(entry.value_per_unit, 631.25)

    def test_save_method_no_valid_per_unit_if_value_is_not_filled(self):
        '''
        `Lot` model entry `save()` method should calculate and fill `value_per_unit` field if data
        is available

        If `value` is not filled, `value_per_unit` should not be calculated
        '''

        # Update the data to include `number_of_units` and remove `value`
        self.lot_data['number_of_units'] = 120
        self.lot_data['value'] = None

        # Create the entry with this updated data
        entry = models.Lot.objects.create(**self.lot_data)

        # `value_per_unit` should be None
        self.assertIsNone(entry.value_per_unit)

    def test_save_method_number_of_units_zero(self):
        '''
        `Lot` model entry `save()` method should calculate and fill `value_per_unit` field if data
        is available

        If `number_of_units` is zero, `value_per_unit` should not be calculated
        '''

        # Update the data to include zero `number_of_units`
        self.lot_data['number_of_units'] = 0

        # Create the entry with this updated data
        entry = models.Lot.objects.create(**self.lot_data)

        # `value_per_unit` should be None
        self.assertIsNone(entry.value_per_unit)

    def test_save_method_reverts_value_per_unit(self):
        '''
        `Lot` model entry `save()` method should calculate and fill `value_per_unit` field if data
        is available

        If `number_of_units` previously exists, and it has been updated to zero or None,
        `value_per_unit` should be updated to None
        '''

        # Update the data to include `number_of_units`
        self.lot_data['number_of_units'] = 11

        # Create the entry with this updated data
        entry = models.Lot.objects.create(**self.lot_data)

        # Update the entry to remove `number_of_units`
        entry.number_of_units = None
        entry.save()

        # `value_per_unit` should be None
        self.assertIsNone(entry.value_per_unit)
