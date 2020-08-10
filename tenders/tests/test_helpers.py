'''
Tests for `tenders.helpers` in the `tenders` Django web application
'''


import datetime
import os
import pytz

from django.conf import settings
from django.test import TestCase

from tenders import helpers, models
from tenders.tests import helpers as t_helpers


class CheckXmlTests(TestCase):
    '''
    TestCase class for the `check_xml` helper function
    '''

    fixtures = [
        './files/initial_data/countries.xml',
        './files/initial_data/currencies.xml'
    ]

    def test_is_valid_false_ted_file_bad_cpv_code(self):
        '''
        `check_xml` should returns (`is_valid` , `error_list`) tuple
        If the input xml `root` does not contain the following:
         * value of CPV_CODE/CODE of `settings.TARGET_CPV_CODE`

        `is_valid` should be `False`

        TED export file 2019-OJS143-352044.xml is valid contract award notice and document type,
        but wrong cpv code
        '''

        # Get the xml root and namespace. File is a valid F03 TED export with incorrect cpv code
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2019-OJS143-352044.xml')
        )

        is_valid, _ = helpers.check_xml(root, n_s)

        #  Confirm `is_valid` is `False`
        self.assertFalse(is_valid)

    def test_raises_error_ted_file_bad_cpv_code(self):
        '''
        `check_xml` should returns (`is_valid` , `error_list`) tuple
        If the input xml `root` does not contain the following:
         * value of CPV_CODE/CODE of `settings.TARGET_CPV_CODE`

        `error_list` should contain an error string

        TED export file 2019-OJS143-352044.xml is valid contract award notice and document type,
        but wrong cpv code
        '''

        # Get the xml root and namespace. File is a valid F03 TED export with incorrect cpv code
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2019-OJS143-352044.xml')
        )

        _, error_list = helpers.check_xml(root, n_s)

        self.assertEqual(
            error_list, ['CPV code is not "' + settings.TARGET_CPV_CODE + '".']
        )

    def test_is_valid_true_ted_file_valid_contract_notice(self):
        '''
        `check_xml` should returns (`is_valid` , `error_list`) tuple
        If the input xml `root` is:
         * A "contract notice" document type
         * A "supplies" contract nature
         * Has a CPV code of `settings.TARGET_CPV_CODE`
         * Is divided into lots

        `is_valid` should be `True`

        TED export file 2019-OJS156-384676.xml is a valid contract notice with the correct
        attributes
        '''

        # Get the xml root and namespace. File is a valid F02 TED export with correct attributes
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2019-OJS156-384676.xml')
        )

        is_valid, _ = helpers.check_xml(root, n_s)

        #  Confirm `is_valid` is `True`
        self.assertTrue(is_valid)

    def test_doesnt_raise_error_ted_file_valid_contract_notice(self):
        '''
        `check_xml` should returns (`is_valid` , `error_list`) tuple
        If the input xml `root` is:
         * A "contract notice" document type
         * A "supplies" contract nature
         * Has a CPV code of `settings.TARGET_CPV_CODE`
         * Is divided into lots

        `error_list` should be an empty list

        TED export file 2019-OJS156-384676.xml is a valid contract notice with the correct
        attributes
        '''

        # Get the xml root and namespace. File is a valid F02 TED export with correct attributes
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2019-OJS156-384676.xml')
        )

        _, error_list = helpers.check_xml(root, n_s)

        # Returned `error_list` should be empty
        self.assertFalse(error_list)

    def test_is_valid_false_contract_award_notice_no_contract_notice(self):
        '''
        `check_xml` should returns (`is_valid` , `error_list`) tuple
        If the input xml `root` is:
         * A "contract award notice" document type
         * A "supplies" contract nature
         * Has a CPV code of `settings.TARGET_CPV_CODE`
         * Is divided into lots

        But input contract award notice has no corresponding contract notice in database,
        `is_valid` should be `False`

        TED export file 2019-OJS072-170256.xml is a valid contract award notice with the correct
        attributes, but no corresponding contract notice in database
        '''

        # Get the xml root and namespace. File is a valid F03 TED export with correct attributes
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2019-OJS072-170256.xml')
        )

        is_valid, _ = helpers.check_xml(root, n_s)

        #  Confirm `is_valid` is `False`
        self.assertFalse(is_valid)

    def test_raises_error_contract_award_notice_no_contract_notice(self):
        '''
        `check_xml` should returns (`is_valid` , `error_list`) tuple
        If the input xml `root` is:
         * A "contract award notice" document type
         * A "supplies" contract nature
         * Has a CPV code of `settings.TARGET_CPV_CODE`
         * Is divided into lots

        But input contract award notice has no corresponding contract notice in database,
        error should be raised

        TED export file 2019-OJS072-170256.xml is a valid contract award notice with the correct
        attributes, but no corresponding contract notice in database
        '''

        # Get the xml root and namespace. File is a valid F03 TED export with correct attributes
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2019-OJS072-170256.xml')
        )

        _, error_list = helpers.check_xml(root, n_s)

        #  Confirm error is raised
        self.assertEqual(
            error_list,
            ['Contract Notice ref "2018/S 191-431371" does not exist in database.']
        )

    def test_is_valid_true_ted_file_contract_award_notice(self):
        '''
        `check_xml` should returns (`is_valid` , `error_list`) tuple
        If the input xml `root` is:
         * A "contract award notice" document type
         * A "supplies" contract nature
         * Has a CPV code of `settings.TARGET_CPV_CODE`
         * Is divided into lots

        `is_valid` should be `True`

        TED export file 2019-OJS072-170256.xml is a valid contract award notice with the correct
        attributes
        '''

        # Upload file needs a corresponding contract notice to return `True`
        # Load 2018/S 191-431371 and associated lots from fixture
        t_helpers.load_fixtures(self, 'test_is_valid_true_ted_file_contract_award_notice.xml')

        # Get the xml root and namespace. File is a valid F03 TED export with correct attributes
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2019-OJS072-170256.xml')
        )

        is_valid, _ = helpers.check_xml(root, n_s)

        #  Confirm `is_valid` is `True`
        self.assertTrue(is_valid)



class GetXmlRootTests(TestCase):
    '''
    TestCase class for the `get_xml_root` helper function
    '''

    def test_root_is_none_if_file_is_invalid(self):
        '''
        `get_xml_root` method should return a tuple containg the xml root and namespaces dictionary
        for the xml file

        If the file is not a valid xml file, the returned tuple should be (`None`, `None`)
        '''

        root, _ = helpers.get_xml_root(os.path.join(settings.TEST_FILES_DIR, 'export.xml'))

        # Confirm `root` is `None`
        self.assertIsNone(root)

    def test_root_is_not_none_if_file_is_valid(self):
        '''
        `get_xml_root` method should return a tuple containg the xml root and namespaces dictionary
        for the xml file

        If the file is a valid xml file, the returned tuple should be (`root`, `ns`)
        '''

        # File is a valid TED export xml file
        root, _ = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2017-OJS184-376771.xml')
        )

        # Confirm `root` is not `None`
        self.assertIsNotNone(root)

    def test_ns_is_not_none_if_file_is_valid(self):
        '''
        `get_xml_root` method should return a tuple containg the xml root and namespaces dictionary
        for the xml file

        If the file is a valid xml file, the returned tuple should be (`root`, `ns`)
        '''

        # File is a valid TED export xml file
        _, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2017-OJS184-376771.xml')
        )

        # Confirm `root` is not `None`
        self.assertIsNotNone(n_s)


class GetTenderClosingDatetimeTests(TestCase):
    '''
    TestCase class for the `get_tender_closing_datetime` helper function
    '''

    def test_method_returns_correct_datetime(self):
        '''
        `get_tender_closing_datetime` should return a datetime object made from
        `F02_DATE_RECEIPT_TENDERS` and `F02_TIME_RECEIPT_TENDERS` data

        If data is found at the xpath locations, method should return a `datetime` object for
        the closing date and time
        '''

        # Get the xml root and namespace. File is a valid F02 TED export with correct attributes
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2019-OJS224-550752.xml')
        )

        returned_datetime = helpers.get_tender_closing_datetime(root, n_s)

        # Closing datetime should be 2019-12-16 10:00
        expected_datetime = datetime.datetime(
            2019, 12, 16, 10, 00, tzinfo=pytz.timezone('Europe/Brussels')
        )

        self.assertEqual(returned_datetime, expected_datetime)

    def test_method_returns_correct_datetime_2(self):
        '''
        `get_tender_closing_datetime` should return a datetime object made from
        `F02_DATE_RECEIPT_TENDERS` and `F02_TIME_RECEIPT_TENDERS` data

        If data is found only at the `F02_DATE_RECEIPT_TENDERS` location, method should return a
        `datetime` object for the closing date
        '''

        # Get the xml root and namespace. File is a valid F02 TED export with correct attributes
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2017-OJS238-493624.xml')
        )

        returned_datetime = helpers.get_tender_closing_datetime(root, n_s)

        # Closing datetime should be 2019-12-16 10:00
        expected_datetime = datetime.datetime(
            2018, 1, 26, 0, 0, tzinfo=pytz.timezone('Europe/Brussels')
        )

        self.assertEqual(returned_datetime, expected_datetime)

    def test_method_returns_none(self):
        '''
        `get_tender_closing_datetime` should return a datetime object made from
        `F02_DATE_RECEIPT_TENDERS` and `F02_TIME_RECEIPT_TENDERS` data

        If data is not found at the xpath locations, method should return `None`
        '''

        # Get the xml root and namespace. File is a F03 TED export that will not have data at the
        # xpath locations
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2019-OJS147-361481.xml')
        )

        returned_datetime = helpers.get_tender_closing_datetime(root, n_s)

        # Closing datetime should be `None`
        self.assertIsNone(returned_datetime)


class GetTenderModelTests(TestCase):
    '''
    TestCase class for the `get_tender_model` helper function
    '''

    def test_method_returns_contract_award_notice_obj(self):
        '''
        `get_tender_model` should return the correct model based on data contained within the
        input `root`

        If `TD_DOCUMENT_TYPE_CODE` is `settings.CONTRACT_AWARD_NOTICE_CODE`, return
        `ContractAwardNotice`
        '''

        # Get the xml root and namespace. File is a valid F03 TED export with correct attributes
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2019-OJS072-170256.xml')
        )

        self.assertEqual(models.ContractAwardNotice, helpers.get_tender_model(root, n_s))

    def test_method_returns_contract_notice_obj(self):
        '''
        `get_tender_model` should return the correct model based on data contained within the
        input `root`

        If `TD_DOCUMENT_TYPE_CODE` is `settings.CONTRACT_NOTICE_CODE`, return `ContractNotice`
        '''

        # Get the xml root and namespace. File is a valid F02 TED export with correct attributes
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2019-OJS156-384676.xml')
        )

        self.assertEqual(models.ContractNotice, helpers.get_tender_model(root, n_s))

    def test_method_returns_none_if_doc_type_code_not_recognised(self):
        '''
        `get_tender_model` should return the correct model based on data contained within the
        input `root`

        If `TD_DOCUMENT_TYPE_CODE` is not a recognised code, return `None`
        '''

        # Get the xml root and namespace. File is a valid F15 TED export with correct attributes
        root, n_s = helpers.get_xml_root(
            os.path.join(settings.TEST_FILES_DIR, '2019-OJS222-544536.xml')
        )

        self.assertIsNone(helpers.get_tender_model(root, n_s))
