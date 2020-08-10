'''
Tests for `tenders.xpaths` in the `tenders` Django web application
'''


import os

from django.conf import settings
from django.test import TestCase

from lxml import etree

from tenders import xpaths
from tenders.helpers import create_namespaces_dict


class XPathTestsF02R209S02E01(TestCase):
    '''
    TestCase class for the `xpath` constants

    These tests are applicable to F02 Contract Notice exports using the R2.0.9.S02.E01 TED
    schema
    '''

    fixtures = ['./files/initial_data/countries.xml', ]

    def setUp(self):
        '''
        Common setup for each test
        '''

        # Create the upload file. File is a valid F02 Contract Notice TED export correct
        # data using the 'R2.0.9.S02.E01' schema
        file_path = os.path.join(settings.TEST_FILES_DIR, '2017-OJS238-493624.xml')

        self.tree = etree.parse(file_path)
        self.root = self.tree.getroot()

        # Replace the default None namespace with one called 'def'
        self.namespaces = create_namespaces_dict(self.root)

        # OBJECT_DESCR element to use with relative xpaths
        self.od_elem = self.root.xpath(xpaths.F02_OBJECT_DESCR, namespaces=self.namespaces)

    def test_date_pub_xpath(self):
        '''
        `DATE_PUB` should return '20171212'
        '''

        result = self.root.xpath(xpaths.DATE_PUB, namespaces=self.namespaces)

        self.assertEqual(result, '20171212')

    def test_ds_date_dispatch_xpath(self):
        '''
        `DS_DATE_DISPATCH` should return '20171207'
        '''

        result = self.root.xpath(xpaths.DS_DATE_DISPATCH, namespaces=self.namespaces)

        self.assertEqual(result, '20171207')

    def test_ia_url_general_xpath(self):
        '''
        `IA_URL_GENERAL` should return 'url'
        '''

        url = 'www.chbm.min-saude.pt'

        result = self.root.xpath(xpaths.IA_URL_GENERAL, namespaces=self.namespaces)

        self.assertEqual(result, url)

    def test_iso_country_value_xpath(self):
        '''
        `ISO_COUNTRY_VALUE` should return 'PT' (Portugal)
        '''

        result = self.root.xpath(xpaths.ISO_COUNTRY_VALUE, namespaces=self.namespaces)

        self.assertEqual(result, 'PT')

    def test_nc_contract_nature_code_xpath(self):
        '''
        `NC_CONTRACT_NATURE_CODE` should return '2' (Supplies)
        '''

        result = self.root.xpath(xpaths.NC_CONTRACT_NATURE_CODE, namespaces=self.namespaces)

        self.assertEqual(result, settings.TARGET_CONTRACT_NATURE_CODE)

    def test_no_doc_ojs_xpath(self):
        '''
        `NO_DOC_OJS` should return '2017/S 238-493624'
        '''

        result = self.root.xpath(xpaths.NO_DOC_OJS, namespaces=self.namespaces)

        self.assertEqual(result, '2017/S 238-493624')

    def test_td_document_type_code_xpath(self):
        '''
        `TD_DOCUMENT_TYPE_CODE` should return '3' (Contract Notice)
        '''

        result = self.root.xpath(xpaths.TD_DOCUMENT_TYPE_CODE, namespaces=self.namespaces)

        self.assertEqual(result, settings.CONTRACT_NOTICE_CODE)

    def test_ted_export_version_xpath(self):
        '''
        `TED_EXPORT_VERSION` should return the export TED schema version

        For this file this should be 'R2.0.9.S02.E01'
        '''

        result = self.root.xpath(xpaths.TED_EXPORT_VERSION, namespaces=self.namespaces)

        self.assertEqual(result, 'R2.0.9.S02.E01')

    def test_uri_doc_xpath(self):
        '''
        `URI_DOC` should return `url`
        '''

        url = 'http://ted.europa.eu/udl?uri=TED:NOTICE:493624-2017:TEXT:PT:HTML'

        result = self.root.xpath(xpaths.URI_DOC, namespaces=self.namespaces)

        self.assertEqual(result, url)

    def test_f02_cpv_code_xpath(self):
        '''
        `F02_CPV_CODE` should return '33600000'
        '''

        result = self.root.xpath(xpaths.F02_CPV_CODE, namespaces=self.namespaces)

        self.assertEqual(result, settings.TARGET_CPV_CODE)

    def test_f02_lot_division_xpath(self):
        '''
        `F02_LOT_DIVISION` should return something to indicate the tender is divided into lots
        '''

        result = self.root.xpath(xpaths.F02_LOT_DIVISION, namespaces=self.namespaces)

        self.assertTrue(result)

    def test_f02_officialname_xpath(self):
        '''
        `F02_OFFICIALNAME` should return `name`
        '''

        name = 'Centro Hospitalar Barreiro Montijo, E.P.E'

        result = self.root.xpath(xpaths.F02_OFFICIALNAME, namespaces=self.namespaces)

        self.assertEqual(result, name)

    def test_f02_short_descr_p_xpath(self):
        '''
        `F02_SHORT_DESCR_P` should return a list of data for the data separated by <P> tags
        '''

        short_descr = ['F10003/2018 - Fornecimento de gases medicinais para o período de 2018 ' + \
                       'a 2019 ao CHBM, E.P.E.']

        result = self.root.xpath(xpaths.F02_SHORT_DESCR_P, namespaces=self.namespaces)

        self.assertEqual(result, short_descr)

    def test_f02_title_p_xpath(self):
        '''
        `F02_TITLE_P` should return `title`
        '''

        title = 'F10003/2018 - Fornecimento de gases medicinais para o período de 2018 ' + \
                'a 2019 ao CHBM, E.P.E.'

        result = self.root.xpath(xpaths.F02_TITLE_P, namespaces=self.namespaces)

        self.assertEqual(result, title)

    def test_f02_document_full_xpath(self):
        '''
        `F02_DOCUMENT_FULL` should return `True`, indicating full documents are available at the
        given url
        '''

        result = self.root.xpath(xpaths.F02_DOCUMENT_FULL, namespaces=self.namespaces)

        self.assertTrue(result)

    def test_f02_url_document_xpath(self):
        '''
        `F02_URL_DOCUMENT` should return a url where the specific details of the procurement can
        be obtained
        '''

        result = self.root.xpath(xpaths.F02_URL_DOCUMENT, namespaces=self.namespaces)

        self.assertEqual(result, 'www.vortalnext.com')

    def test_f02_date_receipt_tenders_xpath(self):
        '''
        `F02_DATE_RECEIPT_TENDERS` should return a date when tenders must be received
        '''

        result = self.root.xpath(xpaths.F02_DATE_RECEIPT_TENDERS, namespaces=self.namespaces)

        self.assertEqual(result, '2018-01-26')


class XPathTestsF02R209S03E01(TestCase):
    '''
    TestCase class for the `xpath` constants

    These tests are applicable to F02 Contract Notice exports using the R2.0.9.S03.E01 TED
    schema
    '''

    fixtures = ['./files/initial_data/countries.xml', ]

    def setUp(self):
        '''
        Common setup for each test
        '''

        # Create the upload file. File is a valid F02 Contract Notice TED export correct
        # data using the 'R2.0.9.S02.E01' schema
        file_path = os.path.join(settings.TEST_FILES_DIR, '2019-OJS156-384676.xml')

        self.tree = etree.parse(file_path)
        self.root = self.tree.getroot()

        # Replace the default None namespace with one called 'def'
        self.namespaces = create_namespaces_dict(self.root)

        # OBJECT_DESCR element to use with relative xpaths
        self.od_elem = self.root.xpath(xpaths.F02_OBJECT_DESCR, namespaces=self.namespaces)

    def test_date_pub_xpath(self):
        '''
        `DATE_PUB` should return '20190814'
        '''

        result = self.root.xpath(xpaths.DATE_PUB, namespaces=self.namespaces)

        self.assertEqual(result, '20190814')

    def test_ds_date_dispatch_xpath(self):
        '''
        `DS_DATE_DISPATCH` should return '20190809'
        '''

        result = self.root.xpath(xpaths.DS_DATE_DISPATCH, namespaces=self.namespaces)

        self.assertEqual(result, '20190809')

    def test_ia_url_general_xpath(self):
        '''
        `IA_URL_GENERAL` should return 'url'
        '''

        url = 'www.zoz-debica.pl'

        result = self.root.xpath(xpaths.IA_URL_GENERAL, namespaces=self.namespaces)

        self.assertEqual(result, url)

    def test_iso_country_value_xpath(self):
        '''
        `ISO_COUNTRY_VALUE` should return 'PL' (Poland)
        '''

        result = self.root.xpath(xpaths.ISO_COUNTRY_VALUE, namespaces=self.namespaces)

        self.assertEqual(result, 'PL')

    def test_nc_contract_nature_code_xpath(self):
        '''
        `NC_CONTRACT_NATURE_CODE` should return '2' (Supplies)
        '''

        result = self.root.xpath(xpaths.NC_CONTRACT_NATURE_CODE, namespaces=self.namespaces)

        self.assertEqual(result, settings.TARGET_CONTRACT_NATURE_CODE)

    def test_no_doc_ojs_xpath(self):
        '''
        `NO_DOC_OJS` should return '2019/S 156-384676'
        '''

        result = self.root.xpath(xpaths.NO_DOC_OJS, namespaces=self.namespaces)

        self.assertEqual(result, '2019/S 156-384676')

    def test_td_document_type_code_xpath(self):
        '''
        `TD_DOCUMENT_TYPE_CODE` should return '3' (Contract Notice)
        '''

        result = self.root.xpath(xpaths.TD_DOCUMENT_TYPE_CODE, namespaces=self.namespaces)

        self.assertEqual(result, settings.CONTRACT_NOTICE_CODE)

    def test_ted_export_version_xpath(self):
        '''
        `TED_EXPORT_VERSION` should return the export TED schema version

        For this file this should be 'R2.0.9.S03.E01'
        '''

        result = self.root.xpath(xpaths.TED_EXPORT_VERSION, namespaces=self.namespaces)

        self.assertEqual(result, 'R2.0.9.S03.E01')

    def test_uri_doc_xpath(self):
        '''
        `URI_DOC` should return `url`
        '''

        url = 'http://ted.europa.eu/udl?uri=TED:NOTICE:384676-2019:TEXT:PL:HTML'

        result = self.root.xpath(xpaths.URI_DOC, namespaces=self.namespaces)

        self.assertEqual(result, url)

    def test_f02_cpv_code_xpath(self):
        '''
        `F02_CPV_CODE` should return '33600000'
        '''

        result = self.root.xpath(xpaths.F02_CPV_CODE, namespaces=self.namespaces)

        self.assertEqual(result, settings.TARGET_CPV_CODE)

    def test_f02_lot_division_xpath(self):
        '''
        `F02_LOT_DIVISION` should return something to indicate the tender is divided into lots
        '''

        result = self.root.xpath(xpaths.F02_LOT_DIVISION, namespaces=self.namespaces)

        self.assertTrue(result)

    def test_f02_officialname_xpath(self):
        '''
        `F02_OFFICIALNAME` should return `name`
        '''

        name = 'Zespół Opieki Zdrowotnej w Dębicy'

        result = self.root.xpath(xpaths.F02_OFFICIALNAME, namespaces=self.namespaces)

        self.assertEqual(result, name)

    def test_f02_short_descr_p_xpath(self):
        '''
        `F02_SHORT_DESCR_P` should return a list of data for the data separated by <P> tags
        '''

        short_descr = [
            'Produkty lecznicze: antybiotyki w pakiecie II, leki oftalmologiczne i ' + \
            'otologiczne w pakiecie IX oraz leki różne w pakiecie X dla apteki szpitalnej ' + \
            'w Zespole Opieki Zdrowotnej w Dębicy'
        ]

        result = self.root.xpath(xpaths.F02_SHORT_DESCR_P, namespaces=self.namespaces)

        self.assertEqual(result, short_descr)

    def test_f02_title_p_xpath(self):
        '''
        `F02_TITLE_P` should return `title`
        '''

        title = 'Produkty lecznicze: antybiotyki w pakiecie II, leki oftalmologiczne i ' + \
                'otologiczne w pakiecie IX oraz leki różne w pakiecie X dla apteki szpitalnej ' + \
                'w Zespole Opieki Zdrowotnej w Dębicy'

        result = self.root.xpath(xpaths.F02_TITLE_P, namespaces=self.namespaces)

        self.assertEqual(result, title)

    def test_f02_document_full_xpath(self):
        '''
        `F02_DOCUMENT_FULL` should return `True`, indicating full documents are available at the
        given url
        '''

        result = self.root.xpath(xpaths.F02_DOCUMENT_FULL, namespaces=self.namespaces)

        self.assertTrue(result)

    def test_f02_url_document_xpath(self):
        '''
        `F02_URL_DOCUMENT` should return a url where the specific details of the procurement can
        be obtained
        '''

        result = self.root.xpath(xpaths.F02_URL_DOCUMENT, namespaces=self.namespaces)

        self.assertEqual(result, 'www.zoz-debica.pl')

    def test_f02_reference_number_xpath(self):
        '''
        `F02_REFERENCE_NUMBER` should return a ref to the specific details of the procurement
        '''

        result = self.root.xpath(xpaths.F02_REFERENCE_NUMBER, namespaces=self.namespaces)

        self.assertEqual(result, 'ZP-PN-49/2019')

    def test_f02_date_receipt_tenders_xpath(self):
        '''
        `F02_DATE_RECEIPT_TENDERS` should return a date when tenders must be received
        '''

        result = self.root.xpath(xpaths.F02_DATE_RECEIPT_TENDERS, namespaces=self.namespaces)

        self.assertEqual(result, '2019-08-26')

    def test_f02_time_receipt_tenders_xpath(self):
        '''
        `F02_TIME_RECEIPT_TENDERS1` should return a time when tenders must be received
        '''

        result = self.root.xpath(xpaths.F02_TIME_RECEIPT_TENDERS, namespaces=self.namespaces)

        self.assertEqual(result, '10:00')


class XPathTestsF03R209S02E01(TestCase):
    '''
    TestCase class for the `xpath` constants

    These tests are applicable to F03 Contract Award Notice exports using the R2.0.9.S02.E01 TED
    schema
    '''

    fixtures = ['./files/initial_data/countries.xml', ]

    def setUp(self):
        '''
        Common setup for each test
        '''

        # Create the upload file. File is a valid F03 Contract Award Notice TED export correct
        # data using the 'R2.0.9.S02.E01' schema
        file_path = os.path.join(settings.TEST_FILES_DIR, '2017-OJS184-376771.xml')

        self.tree = etree.parse(file_path)
        self.root = self.tree.getroot()

        # Replace the default None namespace with one called 'def'
        self.namespaces = create_namespaces_dict(self.root)

        # AWARD_CONTRACT element to use with relative xpaths
        self.ac_elem = self.root.xpath(xpaths.F03_AWARD_CONTRACT, namespaces=self.namespaces)

        # OBJECT_DESCR element to use with relative xpaths
        self.od_elem = self.root.xpath(xpaths.F03_OBJECT_DESCR, namespaces=self.namespaces)

    def test_date_pub_xpath(self):
        '''
        `DATE_PUB` should return '20170926'
        '''

        result = self.root.xpath(xpaths.DATE_PUB, namespaces=self.namespaces)

        self.assertEqual(result, '20170926')

    def test_ds_date_dispatch_xpath(self):
        '''
        `DS_DATE_DISPATCH` should return '20170921'
        '''

        result = self.root.xpath(xpaths.DS_DATE_DISPATCH, namespaces=self.namespaces)

        self.assertEqual(result, '20170921')

    def test_ia_url_general_xpath(self):
        '''
        `IA_URL_GENERAL` should return 'url'
        '''

        url = 'http://www.szpitaltbg.pl'

        result = self.root.xpath(xpaths.IA_URL_GENERAL, namespaces=self.namespaces)

        self.assertEqual(result, url)

    def test_iso_country_value_xpath(self):
        '''
        `ISO_COUNTRY_VALUE` should return 'PL' (Poland)
        '''

        result = self.root.xpath(xpaths.ISO_COUNTRY_VALUE, namespaces=self.namespaces)

        self.assertEqual(result, 'PL')

    def test_nc_contract_nature_code_xpath(self):
        '''
        `NC_CONTRACT_NATURE_CODE` should return '2' (Supplies)
        '''

        result = self.root.xpath(xpaths.NC_CONTRACT_NATURE_CODE, namespaces=self.namespaces)

        self.assertEqual(result, settings.TARGET_CONTRACT_NATURE_CODE)

    def test_no_doc_ojs_xpath(self):
        '''
        `NO_DOC_OJS` should return '2017/S 184-376771'
        '''

        result = self.root.xpath(xpaths.NO_DOC_OJS, namespaces=self.namespaces)

        self.assertEqual(result, '2017/S 184-376771')

    def test_td_document_type_code_xpath(self):
        '''
        `TD_DOCUMENT_TYPE_CODE` should return '7' (Contract Award Notice)
        '''

        result = self.root.xpath(xpaths.TD_DOCUMENT_TYPE_CODE, namespaces=self.namespaces)

        self.assertIn(result, settings.CONTRACT_AWARD_NOTICE_CODE)

    def test_ted_export_version_xpath(self):
        '''
        `TED_EXPORT_VERSION` should return the export TED schema version

        For this file this should be 'R2.0.9.S02.E01'
        '''

        result = self.root.xpath(xpaths.TED_EXPORT_VERSION, namespaces=self.namespaces)

        self.assertEqual(result, 'R2.0.9.S02.E01')

    def test_uri_doc_xpath(self):
        '''
        `URI_DOC` should return `url`
        '''

        url = 'http://ted.europa.eu/udl?uri=TED:NOTICE:376771-2017:TEXT:PL:HTML'

        result = self.root.xpath(xpaths.URI_DOC, namespaces=self.namespaces)

        self.assertEqual(result, url)

    def test_f03_cpv_code_xpath(self):
        '''
        `F03_CPV_CODE` should return '33600000'
        '''

        result = self.root.xpath(xpaths.F03_CPV_CODE, namespaces=self.namespaces)

        self.assertEqual(result, settings.TARGET_CPV_CODE)

    def test_f03_value_xpath(self):
        '''
        `F03_VALUE` should return '4944936.42'
        '''

        result = self.root.xpath(xpaths.F03_VALUE, namespaces=self.namespaces)

        self.assertEqual(result, '4944936.42')

    def test_f03_value_currency_xpath(self):
        '''
        `F03_VALUE_CURRENCY` should return 'PLN' (Polish XXXXXXXXxxx)
        '''

        result = self.root.xpath(xpaths.F03_VALUE_CURRENCY, namespaces=self.namespaces)

        self.assertEqual(result, 'PLN')

    def test_f03_lot_division_xpath(self):
        '''
        `F03_LOT_DIVISION` should return something to indicate the tender is divided into lots
        '''

        result = self.root.xpath(xpaths.F03_LOT_DIVISION, namespaces=self.namespaces)

        self.assertTrue(result)

    def test_f03_officialname_xpath(self):
        '''
        `F03_OFFICIALNAME` should return `name`
        '''

        name = 'Wojewódzki Szpital im. Zofii z Zamoyskich Tarnowskiej w Tarnobrzegu'

        result = self.root.xpath(xpaths.F03_OFFICIALNAME, namespaces=self.namespaces)

        self.assertEqual(result, name)

    def test_f03_short_descr_p_xpath(self):
        '''
        `F03_SHORT_DESCR_P` should return a list of data for the data separated by <P> tags
        '''

        short_descr = [
            'I. Przedmiot zamówienia',
            'Przedmiotem zamówienia jest dostawa leków różnych dla Wojewódzkiego Szpitala im. ' +
            'Zofii z Zamoyskich Tarnowskiej w Tarnobrzegu, ujęta w 44 pakietach.',
            'II. Opis przedmiotu zamówienia:',
            '1. Kod CPV wg Wspólnego Słownika Zamówień:',
            '33600000-6 Produkty farmaceutycznego',
            '33652300-8 Środki immunosupresyjne',
            '33692500-2 Płyny dożylne',
            '33692800-5 Roztwory do dializ',
            '33652100-6 Środki przeciwnowotworowe',
            '33140000-3 Materiały medyczne',
            '2. Szczegółowy opis przedmiotu zamówienia zawiera Załącznik nr 2 do SIWZ – ' +
            'Formularz cenowy.',
            '3. Ilości wskazane w Formularzach cenowych Załącznik nr 2 do SIWZ – są ' +
            'wielkościami orientacyjnymi,przyjętymi dla celu porównania ofert i wyboru ' +
            'najkorzystniejszej oferty. Zamawiający zastrzega sobie prawo zakupu mniejszej ' +
            'ilości przedmiotu zamówienia niż podana',
            'w Formularzu cenowym, w związku z niemożliwością przewidzenia pełnego ' +
            'zapotrzebowania na przedmiot zamówienia objęty niniejszą SIWZ.',
            '4. Zasady realizacji przedmiotowej dostawy określa „Projekt umowy” stan.'
        ]

        result = self.root.xpath(xpaths.F03_SHORT_DESCR_P, namespaces=self.namespaces)

        self.assertEqual(result, short_descr)

    def test_f03_title_p_xpath(self):
        '''
        `F03_TITLE_P` should return `title`
        '''

        title = 'Dostawa leków różnych dla Wojewódzkiego Szpitala im. Zofii z Zamoyskich ' + \
                'Tarnowskiej w Tarnobrzegu.'

        result = self.root.xpath(xpaths.F03_TITLE_P, namespaces=self.namespaces)

        self.assertEqual(result, title)

    def test_award_contract_xpath(self):
        '''
        `F03_AWARD_CONTRACT` should return something to indicate a contract is awarded
        '''

        result = self.root.xpath(xpaths.F03_AWARD_CONTRACT, namespaces=self.namespaces)

        self.assertTrue(result)

    def test_contract_notice_ref_xpath(self):
        '''
        `F03_REF_NOTICE_OJS` should return the ojs ref of the original contract notice linked
        to the tender
        '''

        result = self.root.xpath(xpaths.F03_REF_NOTICE_OJS, namespaces=self.namespaces)

        self.assertEqual(result, '2017/S 107-216084')

    def test_award_contract_lot_no_xpath(self):
        '''
        `LOT_NO` should return the lot number

        For the first lot in the list this should be 1
        '''

        # This is the first lot in the list
        result = self.ac_elem[0].xpath(xpaths.LOT_NO, namespaces=self.namespaces)

        self.assertEqual(result, '1')

    def test_award_contract_lot_awarded_contract_xpath(self):
        '''
        `F03_LOT_AWARDED_CONTRACT` should return something to indicate a contract was awarded for
        the lot

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        # This is the first lot in the list
        result = self.ac_elem[0].xpath(xpaths.F03_LOT_AWARDED_CONTRACT, namespaces=self.namespaces)

        self.assertTrue(result)

    def test_award_contract_lot_awarded_to_group_xpath(self):
        '''
        `F03_LOT_AWARDED_TO_GROUP_R2_0_9_S02_E01` should return something to indicate a contract was
        awarded to a group of contractors

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_AWARDED_TO_GROUP_R2_0_9_S02_E01,
                                       namespaces=self.namespaces)

        self.assertTrue(result)

    def test_award_contract_lot_conclusion_date_xpath(self):
        '''
        `F03_LOT_CONCLUSION_DATE` should return '2017-08-21'

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_CONCLUSION_DATE, namespaces=self.namespaces)

        self.assertEqual(result, '2017-08-21')

    def test_award_contract_lot_contractor_country_xpath(self):
        '''
        `F03_LOT_CONTRACTOR_COUNTRY_R2_0_9_S02_E01` should return 'HU'

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_CONTRACTOR_COUNTRY_R2_0_9_S02_E01,
                                       namespaces=self.namespaces)

        self.assertEqual(result, 'PL')

    def test_award_contract_lot_contractor_name_xpath(self):
        '''
        `F03_LOT_CONTRACTOR_NAME_R2_0_9_S02_E01` should return `name`

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        name = 'Konsorcjum: Farmacol S.A., Farmacol Logistyka Sp. z o. o.'

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_CONTRACTOR_NAME_R2_0_9_S02_E01,
                                       namespaces=self.namespaces)

        self.assertEqual(result, name)

    def test_award_contract_lot_title_xpath(self):
        '''
        `LOT_TITLE_P` should return `title`

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        title = 'Pakiet 1'

        result = self.ac_elem[0].xpath(xpaths.LOT_TITLE_P, namespaces=self.namespaces)

        self.assertEqual(result, title)

    def test_award_contract_lot_val_est_total_xpath(self):
        '''
        `F03_LOT_VAL_EST_TOTAL_R2_0_9_S02_E01` should return '65970.00'

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_VAL_EST_TOTAL_R2_0_9_S02_E01,
                                       namespaces=self.namespaces)

        self.assertEqual(result, '65970.00')

    def test_award_contract_lot_val_est_currency_xpath(self):
        '''
        `F03_LOT_VAL_EST_CURRENCY_R2_0_9_S02_E01` should return 'PLN'

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_VAL_EST_CURRENCY_R2_0_9_S02_E01,
                                       namespaces=self.namespaces)

        self.assertEqual(result, 'PLN')

    def test_award_contract_lot_val_total_xpath(self):
        '''
        `F03_LOT_VAL_TOTAL_R2_0_9_S02_E01` should return '62968.50'

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_VAL_TOTAL_R2_0_9_S02_E01,
                                       namespaces=self.namespaces)

        self.assertEqual(result, '62968.50')

    def test_award_contract_lot_val_total_currency_xpath(self):
        '''
        `F03_LOT_VAL_TOTAL_CURRENCY_R2_0_9_S02_E01` should return 'PLN'

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_VAL_TOTAL_CURRENCY_R2_0_9_S02_E01,
                                       namespaces=self.namespaces)

        self.assertEqual(result, 'PLN')

    def test_object_descr_short_descr_xpath(self):
        '''
        `LOT_SHORT_DESCR_P` should return a list of data for the data separated by <P> tags
        '''

        short_descr = ['Leki immunosupresyjne Ranizimumab.']

        result = self.od_elem[0].xpath(xpaths.LOT_SHORT_DESCR_P, namespaces=self.namespaces)

        self.assertEqual(result, short_descr)


class XPathTestsF03R209S03E01(TestCase):
    '''
    TestCase class for the `xpath` constants

    These tests are applicable to F03 Contract Award Notice exports using the R2.0.9.S03.E01 TED
    schema
    '''

    fixtures = ['./files/initial_data/countries.xml', ]

    def setUp(self):
        '''
        Common setup for each test
        '''

        # Create the upload file. File is a valid TED export correct data using the
        # 'R2.0.9.S03.E01' schema
        file_path = os.path.join(settings.TEST_FILES_DIR, '2019-OJS072-170256.xml')

        self.tree = etree.parse(file_path)
        self.root = self.tree.getroot()

        # Replace the default None namespace with one called 'def'
        self.namespaces = create_namespaces_dict(self.root)

        # AWARD_CONTRACT element to use with relative xpaths
        self.ac_elem = self.root.xpath(xpaths.F03_AWARD_CONTRACT, namespaces=self.namespaces)

        # OBJECT_DESCR element to use with relative xpaths
        self.od_elem = self.root.xpath(xpaths.F03_OBJECT_DESCR, namespaces=self.namespaces)

    def test_date_pub_xpath(self):
        '''
        `DATE_PUB` should return '20170926'
        '''

        result = self.root.xpath(xpaths.DATE_PUB, namespaces=self.namespaces)

        self.assertEqual(result, '20190411')

    def test_ds_date_dispatch_xpath(self):
        '''
        `DS_DATE_DISPATCH` should return '20190409'
        '''

        result = self.root.xpath(xpaths.DS_DATE_DISPATCH, namespaces=self.namespaces)

        self.assertEqual(result, '20190409')

    def test_ia_url_general_xpath(self):
        '''
        `IA_URL_GENERAL` should return 'url'
        '''

        url = 'http://www.bkeok.hu'

        result = self.root.xpath(xpaths.IA_URL_GENERAL, namespaces=self.namespaces)

        self.assertEqual(result, url)

    def test_iso_country_value_xpath(self):
        '''
        `ISO_COUNTRY_VALUE` should return 'HU' (Hungary)
        '''

        result = self.root.xpath(xpaths.ISO_COUNTRY_VALUE, namespaces=self.namespaces)

        self.assertEqual(result, 'HU')

    def test_nc_contract_nature_code_xpath(self):
        '''
        `NC_CONTRACT_NATURE_CODE` should return '2' (Supplies)
        '''

        result = self.root.xpath(xpaths.NC_CONTRACT_NATURE_CODE, namespaces=self.namespaces)

        self.assertEqual(result, settings.TARGET_CONTRACT_NATURE_CODE)

    def test_no_doc_ojs_xpath(self):
        '''
        `NO_DOC_OJS` should return '2017/S 184-376771'
        '''

        result = self.root.xpath(xpaths.NO_DOC_OJS, namespaces=self.namespaces)

        self.assertEqual(result, '2019/S 072-170256')

    def test_td_document_type_code_xpath(self):
        '''
        `TD_DOCUMENT_TYPE_CODE` should return '7' (Contract Award Notice)
        '''

        result = self.root.xpath(xpaths.TD_DOCUMENT_TYPE_CODE, namespaces=self.namespaces)

        self.assertEqual(result, settings.CONTRACT_AWARD_NOTICE_CODE)

    def test_ted_export_version_xpath(self):
        '''
        `TED_EXPORT_VERSION` should return the export TED schema version

        For this file this should be 'R2.0.9.S03.E01'
        '''

        result = self.root.xpath(xpaths.TED_EXPORT_VERSION, namespaces=self.namespaces)

        self.assertEqual(result, 'R2.0.9.S03.E01')

    def test_uri_doc_xpath(self):
        '''
        `URI_DOC` should return `url`
        '''

        url = 'http://ted.europa.eu/udl?uri=TED:NOTICE:170256-2019:TEXT:HU:HTML'

        result = self.root.xpath(xpaths.URI_DOC, namespaces=self.namespaces)

        self.assertEqual(result, url)

    def test_f03_cpv_code_xpath(self):
        '''
        `F03_CPV_CODE` should return '33600000'
        '''

        result = self.root.xpath(xpaths.F03_CPV_CODE, namespaces=self.namespaces)

        self.assertEqual(result, settings.TARGET_CPV_CODE)

    def test_f03_value_xpath(self):
        '''
        `F03_VALUE` should return '387977728'
        '''

        result = self.root.xpath(xpaths.F03_VALUE, namespaces=self.namespaces)

        self.assertEqual(result, '387977728')

    def test_f03_value_currency_xpath(self):
        '''
        `F03_VALUE_CURRENCY` should return 'HUF' (Hungarian Forint)
        '''

        result = self.root.xpath(xpaths.F03_VALUE_CURRENCY, namespaces=self.namespaces)

        self.assertEqual(result, 'HUF')

    def test_f03_lot_division_xpath(self):
        '''
        `F03_LOT_DIVISION` should return something to indicate the tender is divided into lots
        '''

        result = self.root.xpath(xpaths.F03_LOT_DIVISION, namespaces=self.namespaces)

        self.assertTrue(result)

    def test_f03_officialname_xpath(self):
        '''
        `F03_OFFICIALNAME` should return `name`
        '''

        name = 'Borsod-Abaúj-Zemplén Megyei Központi Kórház és Egyetemi Oktatókórház'

        result = self.root.xpath(xpaths.F03_OFFICIALNAME, namespaces=self.namespaces)

        self.assertEqual(result, name)

    def test_f03_short_descr_p_xpath(self):
        '''
        `F03_SHORT_DESCR_P` should return a list of data for the data separated by <P> tags
        '''

        short_descr = [
            'Gyógyszerek és egyéb termékek beszerzése a Borsod-Abaúj-Zemplén Megyei Központi ' +
            'Kórház és Egyetemi Oktatókórházra részére 12+12 hónapos időtartamra.'
        ]

        result = self.root.xpath(xpaths.F03_SHORT_DESCR_P, namespaces=self.namespaces)

        self.assertEqual(result, short_descr)

    def test_f03_title_p_xpath(self):
        '''
        `F03_TITLE_P` should return `title`
        '''

        title = 'Gyógyszerek, egyéb termékek beszerzése BAZ Kórház'

        result = self.root.xpath(xpaths.F03_TITLE_P, namespaces=self.namespaces)

        self.assertEqual(result, title)

    def test_award_contract_xpath(self):
        '''
        `F03_AWARD_CONTRACT` should return something to indicate a contract is awarded
        '''

        result = self.root.xpath(xpaths.F03_AWARD_CONTRACT, namespaces=self.namespaces)

        self.assertTrue(result)

    def test_contract_notice_ref_xpath(self):
        '''
        `F03_REF_NOTICE_OJS` should return the ojs ref of the original contract notice linked
        to the tender
        '''

        result = self.root.xpath(xpaths.F03_REF_NOTICE_OJS, namespaces=self.namespaces)

        self.assertEqual(result, '2018/S 191-431371')

    def test_award_contract_lot_no_xpath(self):
        '''
        `LOT_NO` should return the lot number

        For the first lot in the list this should be 1
        '''

        # This is the first F03_LOT in the list
        result = self.ac_elem[0].xpath(xpaths.LOT_NO, namespaces=self.namespaces)

        self.assertEqual(result, '1')

    def test_award_contract_lot_awarded_contract_xpath(self):
        '''
        `F03_LOT_AWARDED_CONTRACT` should return something to indicate a contract was awarded for
        the lot

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        # This is the first lot in the list
        result = self.ac_elem[0].xpath(xpaths.F03_LOT_AWARDED_CONTRACT, namespaces=self.namespaces)

        self.assertTrue(result)

    def test_award_contract_lot_awarded_to_group_xpath(self):
        '''
        `F03_LOT_AWARDED_TO_GROUP_R2_0_9_S03_E01` should return something to indicate a contract was
        awarded to a group of contractors

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_AWARDED_TO_GROUP_R2_0_9_S03_E01,
                                       namespaces=self.namespaces)

        self.assertTrue(result)

    def test_award_contract_lot_conclusion_date_xpath(self):
        '''
        `F03_LOT_CONCLUSION_DATE` should return '2019-02-15'

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_CONCLUSION_DATE, namespaces=self.namespaces)

        self.assertEqual(result, '2019-02-15')

    def test_award_contract_lot_contractor_country_xpath(self):
        '''
        `F03_LOT_CONTRACTOR_COUNTRY_R2_0_9_S03_E01` should return 'HU'

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_CONTRACTOR_COUNTRY_R2_0_9_S03_E01,
                                       namespaces=self.namespaces)

        self.assertEqual(result, 'HU')

    def test_award_contract_lot_contractor_name_xpath(self):
        '''
        `F03_LOT_CONTRACTOR_NAME_R2_0_9_S03_E01` should return `name`

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        name = 'HUNGAROPHARMA Gyógyszerkereskedelmi Zártkörűen Működő Részvénytársaság'

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_CONTRACTOR_NAME_R2_0_9_S03_E01,
                                       namespaces=self.namespaces)

        self.assertEqual(result, name)

    def test_award_contract_lot_title_xpath(self):
        '''
        `LOT_TITLE_P` should return `title`

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        title = 'Gyógyszerek és egyéb termékek beszerzése'

        result = self.ac_elem[0].xpath(xpaths.LOT_TITLE_P, namespaces=self.namespaces)

        self.assertEqual(result, title)

    def test_award_contract_lot_val_est_total_xpath(self):
        '''
        `F03_LOT_VAL_EST_TOTAL_R2_0_9_S03_E01` should return '38439512'

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_VAL_EST_TOTAL_R2_0_9_S03_E01,
                                       namespaces=self.namespaces)

        self.assertEqual(result, '254661482')

    def test_award_contract_lot_val_est_currency_xpath(self):
        '''
        `F03_LOT_VAL_EST_CURRENCY_R2_0_9_S03_E01` should return 'HUF'

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_VAL_EST_CURRENCY_R2_0_9_S03_E01,
                                       namespaces=self.namespaces)

        self.assertEqual(result, 'HUF')

    def test_award_contract_lot_val_total_xpath(self):
        '''
        `F03_LOT_VAL_TOTAL_R2_0_9_S03_E01` should return '38439512'

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_VAL_TOTAL_R2_0_9_S03_E01,
                                       namespaces=self.namespaces)

        self.assertEqual(result, '38439512')

    def test_award_contract_lot_val_total_currency_xpath(self):
        '''
        `F03_LOT_VAL_TOTAL_CURRENCY_R2_0_9_S03_E01` should return 'HUF'

        This path is different across the supported schemas

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_VAL_TOTAL_CURRENCY_R2_0_9_S03_E01,
                                       namespaces=self.namespaces)

        self.assertEqual(result, 'HUF')

    def test_object_descr_short_descr_xpath(self):
        '''
        `LOT_SHORT_DESCR_P` should return a list of data for the data separated by <P> tags
        '''

        short_descr = [
            'II.2.4) A közbeszerzés ismertetése:',
            '(az építési beruházás, árubeszerzés vagy szolgáltatás jellege és mennyisége, ' +
            'illetve az igények és követelmények meghatározása)',
            'Különbőzó gyógyszerek, és gyógyhatású termékeke beszerzése különböző hatóanyaggal, ' +
            'és kiszerelésben a dokumentációban részletezettek szerint, tekintettel arra, hogy ' +
            'az EKR rendszerbe a karakter korlátozás miatt a beszerzendő termékek és mennyiségek ' +
            'nem sorolhatók fel.',
            'A hivatalos nagykerereskedelmi árral rendelkező készítményeknél az ajánlati ár a ' +
            'nagykereskedelmi árnál magasabb nem lehet.',
            'A dokumetnáció mellékletét képező "Részletező ártáblázat" nevezetű dokumentációt ' +
            'kérjük maradéktalanul kitölteni, az ajánlatok összehasonlítása és bírálata ' +
            'hatóanyagonként történik.'
        ]

        result = self.od_elem[0].xpath(xpaths.LOT_SHORT_DESCR_P, namespaces=self.namespaces)

        self.assertEqual(result, short_descr)


class XPathTestsF03R209S03E012(TestCase):
    '''
    TestCase class for the `xpath` constants

    These tests are applicable to F03 Contract Award Notice exports using the R2.0.9.S03.E01 TED
    schema

    Using 2019-OJS147-361501.xml to test unusual paths work
    '''

    fixtures = ['./files/initial_data/countries.xml', ]

    def setUp(self):
        '''
        Common setup for each test
        '''

        # Create the upload file. File is a valid TED export correct data
        file_path = os.path.join(settings.TEST_FILES_DIR, '2019-OJS147-361501.xml')

        self.tree = etree.parse(file_path)
        self.root = self.tree.getroot()

        # Replace the default None namespace with one called 'def'
        self.namespaces = create_namespaces_dict(self.root)

        # AWARD_CONTRACT element to use with relative xpaths
        self.ac_elem = self.root.xpath(xpaths.F03_AWARD_CONTRACT, namespaces=self.namespaces)

        # OBJECT_DESCR element to use with relative xpaths
        self.od_elem = self.root.xpath(xpaths.F03_OBJECT_DESCR, namespaces=self.namespaces)

    def test_lot_val_range_low_xpath(self):
        '''
        `F03_LOT_VAL_RANGE_LOW` should return '957307.18'

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_VAL_RANGE_LOW, namespaces=self.namespaces)

        self.assertEqual(result, '957307.18')

    def test_lot_val_range_high_xpath(self):
        '''
        `F03_LOT_VAL_RANGE_HIGH` should return '957307.18'

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_VAL_RANGE_HIGH, namespaces=self.namespaces)

        self.assertEqual(result, '957307.18')

    def test_lot_val_range_currency_xpath(self):
        '''
        `F03_LOT_VAL_RANGE_CURRENCY` should return 'RON'

        xpath is local to element returned from `AWARD_CONTRACT`
        '''

        result = self.ac_elem[0].xpath(xpaths.F03_LOT_VAL_RANGE_CURRENCY,
                                       namespaces=self.namespaces)

        self.assertEqual(result, 'RON')

    def test_object_descr_info_add_xpath(self):
        '''
        `LOT_INFO_ADD_P` should return a list of data for the data separated by <P> tags
        '''

        info_add = [
            'Valoarea estimata a celui mai mare contract subsecvent – lot 2 – este de 478 653,65 ' +
            'RON.',
            'Valoarea estimata a celui mai mic contract subsecvent – lot 2 – este de 239 326,82 ' +
            'RON.'
        ]

        result = self.od_elem[0].xpath(xpaths.LOT_INFO_ADD_P, namespaces=self.namespaces)

        self.assertEqual(result, info_add)
