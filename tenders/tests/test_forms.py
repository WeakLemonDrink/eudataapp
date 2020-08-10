'''
Tests for `tenders.forms` in the `tenders` Django web application
'''


import os

from django.conf import settings
from django.test import TestCase

from tasks.models import DailyPackageDownloadStatus
from tenders import models
from tenders import forms
from tenders.tests import helpers


class UploadXmlFileFormTests(TestCase):
    '''
    TestCase class for the `UploadXmlFileForm` form
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
        self.post_data = {}

        # Create some empty files to test raising errors
        self.empty_xml_file = helpers.create_files_data('export.xml')

    def test_form_init_saves_upload_file_to_tmp(self):
        '''
        `UploadXmlFileForm` `__init__()` method should save a xml file in `request.FILES` to a
        temporary location for use in `.clean()` and `.save()` methods

        `__init__()` method should save the file to a path defined by `settings.TEMP_FILES_DIR`
        and the file name, and store the path to `upload_file_path`
        '''

        # Instantiate the form
        form = forms.UploadXmlFileForm(self.post_data, self.empty_xml_file)

        # Confirm the file has been saved to the `settings.TEMP_FILES_DIR` location
        self.assertTrue(os.path.isfile(form.upload_file_path))

    def test_form_del_removes_file_from_temp(self):
        '''
        `UploadXmlFileForm` `__del__()` method should remove a file saved to the `upload_file_path`
        location when the class instance is destroyed
        '''

        # Instantiate the form
        form = forms.UploadXmlFileForm(self.post_data, self.empty_xml_file)

        upload_file_path = form.upload_file_path

        # Delete the form, which should call the `__del__()` method
        del form

        # Confirm the file has been removed from the `upload_file_path` location
        self.assertFalse(os.path.isfile(upload_file_path))

    def test_from_raises_error_bad_upload_file_upload(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should raise an error if the uploaded file is
        an invalid xml file

        If the file has an .xml extension, but it is empty or doesn't have the correct structure,
        an error should be raised attached to the `upload_file` field
        '''

        file_name = 'export.xml'

        upload_file = helpers.create_files_data(file_name)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['upload_file'], ['"' + file_name + '" file contains invalid syntax.']
        )

    def test_form_is_valid_false_ted_file_bad_contract_type(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should return `False` if the uploaded file is a
        valid xml file, but doesn't contain a valid cpv code

        If the xml file does not contain the following:
         * tag TYPE_CONTRACT with the attribute CTYPE
         * value of TYPE_CONTRACT/CTYPE of `settings.TARGET_CONTRACT_TYPE`

        `.is_valid() should return `False`

        TED export file 2019-OJS115-281492.xml is valid cpv code and document type, but wrong
        contract type
        '''

        # Create the upload file. File is a valid F03 TED export with incorrect contract type
        upload_file = helpers.create_files_data('2019-OJS115-281492.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        #  Confirm `.is_valid()` method returns `False`
        self.assertFalse(form.is_valid())

    def test_from_raises_error_ted_file_bad_contract_type(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should raise an error if the uploaded file is a
        valid xml file, but doesn't contain a valid document type

        If the xml file does not contain the following:
         * tag TD_DOCUMENT_TYPE with the attribute CODE
         * value of TD_DOCUMENT_TYPE/CODE of 7 (Contract award notice)

        `.is_valid() should return `False`

        TED export file 2019-OJS115-281492.xml is valid cpv code and document type, but wrong
        contract type
        '''

        # Create the upload file. File is a valid F03 TED export with incorrect contract type
        upload_file = helpers.create_files_data('2019-OJS115-281492.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['upload_file'],
            ['Contract nature is not "' + settings.TARGET_CONTRACT_NATURE_CODE + '".']
        )

    def test_form_is_valid_false_f02_ted_file_bad_cpv_code(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should return `False` if the uploaded file is a
        valid xml file, but doesn't contain a valid cpv code

        If the xml file does not contain the following:
         * tag CPV_CODE with the attribute CODE
         * value of CPV_CODE/CODE of `settings.TARGET_CPV_CODE`

        `.is_valid() should return `False`

        TED export file 2019-OJS224-550752.xml is valid contract type and document type, but wrong
        cpv code
        '''

        # Create the upload file. File is a valid F02 TED export with incorrect cpv code
        upload_file = helpers.create_files_data('2019-OJS224-550752.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        #  Confirm `.is_valid()` method returns `False`
        self.assertFalse(form.is_valid())

    def test_from_raises_error_f02_ted_file_bad_cpv_code(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should raise an error if the uploaded file is a
        valid xml file, but doesn't contain a valid cpv code

        If the xml file does not contain the following:
         * tag CPV_CODE with the attribute CODE
         * value of CPV_CODE/CODE of `settings.TARGET_CPV_CODE`

        `.is_valid() should return `False`

        TED export file 2019-OJS224-550752.xml is valid contract type and document type, but wrong
        cpv code.
        '''

        # Create the upload file. File is a valid F02 TED export with incorrect cpv code
        upload_file = helpers.create_files_data('2019-OJS224-550752.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['upload_file'], ['CPV code is not "' + settings.TARGET_CPV_CODE + '".']
        )

    def test_form_is_valid_false_f02_ted_file_no_lot_division(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should return `False` if the uploaded file is a
        valid xml file, but the contract award notice isn't divided into lots

        If the xml file does not contain the following:
         * tag LOT_DIVISION

        `.is_valid() should return `False`

        TED export file 2019-OJS224-549059.xml is valid contract type and document type, but is not
        divided into lots
        '''

        # Create the upload file. File is a valid F02 TED export with no LOT_DIVISION tag
        upload_file = helpers.create_files_data('2019-OJS224-549059.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        #  Confirm `.is_valid()` method returns `False`
        self.assertFalse(form.is_valid())

    def test_from_raises_error_f02_ted_file_no_lot_division(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should return `False` if the uploaded file is a
        valid xml file, but the tender isn't divided into lots

        If the xml file does not contain the following:
         * tag LOT_DIVISION

        the form should raise an error on clean

        TED export file 2019-OJS224-549059.xml is valid contract type and document type, but is not
        divided into lots
        '''

        # Create the upload file. File is a valid F02 TED export with no LOT_DIVISION tag
        upload_file = helpers.create_files_data('2019-OJS224-549059.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['upload_file'], ['Contract Notice is not divided into Lots.']
        )

    def test_from_raises_error_f03_ted_file_bad_cpv_code(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should raise an error if the uploaded file is a
        valid xml file, but doesn't contain a valid cpv code

        If the xml file does not contain the following:
         * tag CPV_CODE with the attribute CODE
         * value of CPV_CODE/CODE of `settings.TARGET_CPV_CODE`

        `.is_valid() should return `False`

        TED export file 2019-OJS143-352044.xml is valid contract type and document type, but wrong
        cpv code.
        '''

        # Create the upload file. File is a valid F03 TED export with incorrect cpv code
        upload_file = helpers.create_files_data('2019-OJS143-352044.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['upload_file'], ['CPV code is not "' + settings.TARGET_CPV_CODE + '".']
        )

    def test_form_is_valid_false_f03_ted_file_no_lot_division(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should return `False` if the uploaded file is a
        valid xml file, but the contract award notice isn't divided into lots

        If the xml file does not contain the following:
         * tag LOT_DIVISION

        `.is_valid() should return `False`

        TED export file 2019-OJS138-339819.xml is valid contract type and document type, but is not
        divided into lots
        '''

        # Create the upload file. File is a valid F03 TED export with no LOT_DIVISION tag
        upload_file = helpers.create_files_data('2019-OJS138-339819.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        #  Confirm `.is_valid()` method returns `False`
        self.assertFalse(form.is_valid())

    def test_from_raises_error_f03_ted_file_no_lot_division(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should return `False` if the uploaded file is a
        valid xml file, but the contract award notice isn't divided into lots

        If the xml file does not contain the following:
         * tag LOT_DIVISION

        the form should raise an error on clean

        TED export file 2019-OJS138-339819.xml is valid contract type and document type, but is not
        divided into lots
        '''

        # Create the upload file. File is a valid F03 TED export with no LOT_DIVISION tag
        upload_file = helpers.create_files_data('2019-OJS138-339819.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['upload_file'], ['Contract Award Notice is not divided into Lots.']
        )

    def test_form_is_valid_true_f02_ted_file(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should return `True` if the uploaded file is a
        valid xml file and contains valid cpv code and contract type

        If the xml file does contains the following:
         * tag CPV_CODE with the attribute CODE
         * value of CPV_CODE/CODE of `settings.TARGET_CPV_CODE`
         * tag TYPE_CONTRACT with the attribute CTYPE
         * value of TYPE_CONTRACT/CTYPE of `settings.TARGET_CONTRACT_TYPE`

        `.is_valid() should return `True`

        TED export file 2019-OJS156-384676.xml is valid cpv code, document type and contract type
        '''

        # Create the upload file. File is a valid F02 TED export correct data
        upload_file = helpers.create_files_data('2019-OJS156-384676.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        #  Confirm `.is_valid()` method returns `True`
        self.assertTrue(form.is_valid())

    def test_form_is_valid_true_f03_ted_file(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should return `True` if the uploaded file is a
        valid xml file and contains valid cpv code and contract type

        If the xml file does contains the following:
         * tag CPV_CODE with the attribute CODE
         * value of CPV_CODE/CODE of `settings.TARGET_CPV_CODE`
         * tag TYPE_CONTRACT with the attribute CTYPE
         * value of TYPE_CONTRACT/CTYPE of `settings.TARGET_CONTRACT_TYPE`

        `.is_valid() should return `True`

        TED export file 2019-OJS072-170256.xml is valid cpv code, document type and contract type
        '''

        # Upload file needs a corresponding contract notice for `is_valid()` to return `True`
        # Load 2018/S 191-431371 and associated lots from fixture
        helpers.load_fixtures(self, 'test_form_is_valid_true_f03_ted_file.xml')

        # Create the upload file. File is a valid F03 TED export correct data
        upload_file = helpers.create_files_data('2019-OJS072-170256.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        #  Confirm `.is_valid()` method returns `True`
        self.assertTrue(form.is_valid())

    def test_form_is_valid_false_f02_existing_data(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should return `False` if the uploaded file is a
        valid xml file with correct attributes, but we already have this data

        If the xml file `ojs_ref` attribute matches a `ContractNotice` entry `.is_valid()
        should return `False`

        TED export file 2019-OJS156-384676.xml is valid cpv code, document type and contract type
        '''

        # Create new `ContractNotice` entry with the same `ojs_ref` as the uploaded file
        # Load 2019/S 156-384676 and associated lots from fixture
        helpers.load_fixtures(self, 'test_form_f02_existing_data.xml')

        # Create the upload file. File is a valid F02 TED export correct data
        upload_file = helpers.create_files_data('2019-OJS156-384676.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        #  Confirm `.is_valid()` method returns `False`
        self.assertFalse(form.is_valid())

    def test_from_raises_error_f02_existing_data(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should raise an error if the uploaded file is a
        valid xml file with correct attributes, but we already have this data

        If the xml file `ojs_ref` attribute matches a `ContractNotice` entry `.is_valid() should
        return `False`

        TED export file 2019-OJS156-384676.xml is valid cpv code, document type and contract type
        '''

        # Create new `ContractNotice` entry with the same `ojs_ref` as the uploaded file
        # Load 2019/S 156-384676 and associated lots from fixture
        helpers.load_fixtures(self, 'test_form_f02_existing_data.xml')

        # Create the upload file. File is a valid F02 TED export correct data
        upload_file = helpers.create_files_data('2019-OJS156-384676.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['upload_file'],
            ['Contract Notice ref "2019/S 156-384676" already exists in database.']
        )

    def test_form_is_valid_false_f03_existing_data(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should return `False` if the uploaded file is a
        valid xml file with correct attributes, but we already have this data

        If the xml file `ojs_ref` attribute matches a `ContractAwardNotice` entry `.is_valid()
        should return `False`

        TED export file 2019-OJS072-170256.xml is valid cpv code, document type and contract type
        '''

        # Create new `ContractAwardNotice` entry with the same `ojs_ref` as the uploaded file
        # Load 2019/S 072-170256 and associated contract notice and lots from fixture
        helpers.load_fixtures(self, 'test_form_f03_existing_data.xml')

        # Create the upload file. File is a valid F03 TED export correct data
        upload_file = helpers.create_files_data('2019-OJS072-170256.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        #  Confirm `.is_valid()` method returns `False`
        self.assertFalse(form.is_valid())

    def test_from_raises_error_f03_existing_data(self):
        '''
        `UploadXmlFileForm` `.is_valid()` method should raise an error if the uploaded file is a
        valid xml file with correct attributes, but we already have this data

        If the xml file `ojs_ref` attribute matches a `ContractAwardNotice` entry `.is_valid()
        should return `False`

        TED export file 2019-OJS072-170256.xml is valid cpv code, document type and contract type
        '''

        # Create new `ContractAwardNotice` entry with the same `ojs_ref` as the uploaded file
        # Load 2019/S 072-170256 and associated contract notice and lots from fixture
        helpers.load_fixtures(self, 'test_form_f03_existing_data.xml')

        # Create the upload file. File is a valid F03 TED export correct data
        upload_file = helpers.create_files_data('2019-OJS072-170256.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['upload_file'],
            ['Contract Award Notice ref "2019/S 072-170256" already exists in database.']
        )

    def test_form_save_save_new_f02_entry(self):
        '''
        `UploadXmlFileForm` `.save()` method should save data to a new `ContractNotice` entry if
        the uploaded file is a valid xml file with correct attributes

        TED export file 2017-OJS238-493624.xml is valid cpv code, document type and contract type
        '''

        # Create the upload file. File is a valid F02 TED export correct data
        upload_file = helpers.create_files_data('2017-OJS238-493624.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Call `.is_valid()` first
        form.is_valid()

        new_entry = form.save()

        # New entry should be ref 2017/S 238-493624
        self.assertEqual(str(new_entry), '2017/S 238-493624')

    def test_form_save_f03_new_contract_award_notice_entry(self):
        '''
        `UploadXmlFileForm` `.save()` method should save data to a new `ContractAwardNotice` entry
        if the uploaded file is a valid xml file with correct attributes

        TED export file 2019-OJS097-234233.xml is valid cpv code, document type and contract type
        '''

        # Upload file needs a corresponding contract notice for `is_valid()` to return `True`
        # Load 2018/S 244-557823 and associated lots from fixture
        helpers.load_fixtures(self, 'test_form_save_save_new_f03_entry.xml')

        # Create the upload file. File is a valid F03 TED export correct data
        upload_file = helpers.create_files_data('2019-OJS097-234233.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Call `.is_valid()` first
        form.is_valid()

        new_entry = form.save()

        # New entry should be ref 2019/S 097-234233
        self.assertEqual(str(new_entry), '2019/S 097-234233')

    def test_form_save_f03_updates_lots(self):
        '''
        `UploadXmlFileForm` `.save()` method should save data to a new `ContractAwardNotice` entry
        if the uploaded file is a valid xml file with correct attributes

        Existing `lots`s linked to the referenced `ContractNotice` should also be updated with
        value information

        TED export file 2019-OJS097-234233.xml is valid cpv code, document type and contract type
        '''

        # Upload file needs a corresponding contract notice for `is_valid()` to return `True`
        # Load 2018/S 244-557823 and associated lots from fixture
        helpers.load_fixtures(self, 'test_form_save_save_new_f03_entry.xml')

        # Create the upload file. File is a valid F03 TED export correct data
        upload_file = helpers.create_files_data('2019-OJS097-234233.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Call `.is_valid()` first
        form.is_valid()

        form.save()

        # Lots should be updated to contain value information
        contract_notice = models.ContractNotice.objects.get(ojs_ref='2018/S 244-557823')

        # 128 lots have awarded contract, and so should have the value filled
        self.assertEqual(contract_notice.lot_set.filter(value__isnull=False).count(), 128)

    def test_form_save_f02_new_lot_entries_total_lots(self):
        '''
        `UploadXmlFileForm` `.save()` method should save data to a new `ContractNotice`
        entry and related `Lot` entries if the uploaded file is a valid xml file with
        correct attributes

        TED export file 2018-OJS244-557823.xml is valid cpv code, document type and contract type

        Uploaded contract notice has 143 lots that have a valid title and not awarded to a group
        '''

        # Create the upload file. File is a valid F02 TED export correct data
        upload_file = helpers.create_files_data('2018-OJS244-557823.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Call `.is_valid()` first
        form.is_valid()

        new_tender_entry = form.save()

        # new_tender_entry should have a total of 143 lots associated with it
        self.assertEqual(new_tender_entry.lot_set.count(), 143)

    def test_form_save_f03_new_ted_entry_2(self):
        '''
        `UploadXmlFileForm` `.save()` method should save data to a new `ContractAwardNotice`
        entry if the uploaded file is a valid xml file with correct attributes

        TED export file 2019-OJS147-361791.xml is valid cpv code, document type and contract type
        '''

        # Upload file needs a corresponding contract notice for `is_valid()` to return `True`
        # Load 2018/S 208-474350 and associated lots from fixture
        helpers.load_fixtures(self, 'test_form_save_save_new_ted_entry_2.xml')

        # Create the upload file. File is a valid F03 TED export correct data
        upload_file = helpers.create_files_data('2019-OJS147-361791.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Call `.is_valid()` first
        form.is_valid()

        new_entry = form.save()

        # New entry should be ref 2019/S 147-361791
        self.assertEqual(str(new_entry), '2019/S 147-361791')

    def test_form_save_f02_new_lot_entries_total_lots_2(self):
        '''
        `UploadXmlFileForm` `.save()` method should save data to a new `ContractAwardNotice`
        entry and related `Lot` entries if the uploaded file is a valid xml file with correct
        attributes

        TED export file 2018-OJS208-474350.xml is valid cpv code, document type and contract type

        Uploaded tender has 75 lots that are contract awarded and not awarded to a group
        '''

        # Create the upload file. File is a valid F02 TED export correct data
        upload_file = helpers.create_files_data('2018-OJS208-474350.xml', settings.TEST_FILES_DIR)

        form = forms.UploadXmlFileForm(self.post_data, upload_file)

        # Call `.is_valid()` first
        form.is_valid()

        new_tender_entry = form.save()

        # new_tender_entry should have a total of 75 valid lots associated with it
        self.assertEqual(new_tender_entry.lot_set.count(), 75)


class DailyPackageDownloadFormTests(TestCase):
    '''
    TestCase class for the `DailyPackageDownloadForm` form
    '''

    def setUp(self):
        '''
        Common setup for each test
        '''

        # Create a `DailyPackageDownloadStatus` entry to check against
        DailyPackageDownloadStatus.objects.create(
            file_name='20190916_2019178.tar.gz', status=DailyPackageDownloadStatus.COMPLETE
        )

    def test_form_is_valid_false_date_has_already_been_processed(self):
        '''
        `DailyPackageDownloadForm` `.is_valid()` method should return `False` if a daily package
        file has already been processed

        If the file has already been processed, there will be a entry in the
        `DailyPackageDownloadStatus` model recording this. If the status is COMPLETE, the file
        should not be processed again
        '''

        # Instantiate the form with a valid date in past
        form = forms.DailyPackageDownloadForm({'date': '16/09/2019'})

        # Confirm `.is_valid()` method returns `False`
        self.assertFalse(form.is_valid())

    def test_from_raises_error_date_has_already_been_processed(self):
        '''
        `DailyPackageDownloadForm` `.clean()` method should raise an error if a daily package
        file has already been processed

        If the file has already been processed, there will be a entry in the
        `DailyPackageDownloadStatus` model recording this. If the status is COMPLETE, the file
        should not be processed again
        '''

        # Instantiate the form with a valid date in past
        form = forms.DailyPackageDownloadForm({'date': '16/09/2019'})

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['date'], ['Daily package for this date has already been downloaded.']
        )

    def test_form_is_valid_false_no_daily_package_file_for_date(self):
        '''
        `DailyPackageDownloadForm` `.is_valid()` method should return `False` if a daily package
        file is not available on the ftp server for the input date
        '''

        # Instantiate the form with a date in the future
        form = forms.DailyPackageDownloadForm({'date': '16/09/2119'})

        # Confirm `.is_valid()` method returns `False`
        self.assertFalse(form.is_valid())

    def test_from_raises_error_no_daily_package_file_for_date(self):
        '''
        `DailyPackageDownloadForm` `.clean()` method should raise an error if a daily package
        file is not available on the ftp server for the input date
        '''

        # Instantiate the form with a date in the future
        form = forms.DailyPackageDownloadForm({'date': '16/09/2119'})

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['date'],
            ['Daily package for this date is not available on the ftp server.']
        )

    def test_form_is_valid_true_daily_package_file_available_for_date(self):
        '''
        `DailyPackageDownloadForm` `.is_valid()` method should return `True` if a daily package
        file is available on the ftp server for the input date
        '''

        # Instantiate the form with a date in the future
        form = forms.DailyPackageDownloadForm({'date': '13/09/2019'})

        # Confirm `.is_valid()` method returns `True`
        self.assertTrue(form.is_valid())

    def test_form_is_valid_false_date_has_already_been_processed(self):
        '''
        `DailyPackageDownloadForm` `.is_valid()` method should return `False` if a daily package
        file has already been processed

        If the file has already been processed, there will be a entry in the
        `DailyPackageDownloadStatus` model recording this. If the status is not COMPLETE (e.g. 
        TIMEOUT or ERROR) we should allow it to be processed again.
        '''

        # Get the `DailyPackageDownloadStatus` entry and set the status to TIMEOUT
        task_status = DailyPackageDownloadStatus.objects.get(file_name='20190916_2019178.tar.gz')
        task_status.set_status(DailyPackageDownloadStatus.TIMEOUT)

        # Instantiate the form with a valid date in past
        form = forms.DailyPackageDownloadForm({'date': '16/09/2019'})

        # Confirm `.is_valid()` method returns `True`
        self.assertTrue(form.is_valid())
