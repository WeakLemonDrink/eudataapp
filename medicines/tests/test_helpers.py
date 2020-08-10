'''
Tests for the `medicines` Django web application
'''


import json
import os

from django.conf import settings
from django.test import TestCase

from medicines.helpers import process_pricing_data


class ProcessPricingDataTests(TestCase):
    '''
    TestCase class for the `process_pricing_data` helper
    '''

    def test_process_pricing_data_valid_data_returns_list(self):
        '''
        `process_pricing_data` helper function should return `price_per_unit` data as a list of
        dictionaries

        '0212000AAAAABAB.json' is valid data returned from the Open Prescribing api
        '''

        with open(os.path.join(settings.TEST_FILES_DIR, '0212000AAAAABAB.json')) as file:
            raw_data = json.load(file)

        pricing_data = process_pricing_data(raw_data)

        self.assertTrue(isinstance(pricing_data, list))

    def test_process_pricing_data_valid_data_returns_price_per_unit(self):
        '''
        `process_pricing_data` helper function should return `price_per_unit` data as a list of
        dictionaries, and each dict should contain `date` and `price_per_unit` keys

        '0212000AAAAABAB.json' is valid data returned from the Open Prescribing api
        '''

        with open(os.path.join(settings.TEST_FILES_DIR, '0212000AAAAABAB.json')) as file:
            raw_data = json.load(file)

        pricing_data = process_pricing_data(raw_data)

        # Check `price_per_unit` key is in the first dict
        self.assertTrue('price_per_unit' in pricing_data[0])

    def test_process_pricing_data_data_results_in_divide_by_zero(self):
        '''
        `process_pricing_data` helper function should return `price_per_unit` data as a list of
        dictionaries, and each dict should contain `date` and `price_per_unit` keys

        '0101010I0BFAAAE.json' is valid data returned from the Open Prescribing api, but contains
        some entries with `quantity=0` which would cause divide by zero errors if not handled
        properly
        '''

        with open(os.path.join(settings.TEST_FILES_DIR, '0101010I0BFAAAE.json')) as file:
            raw_data = json.load(file)

        pricing_data = process_pricing_data(raw_data)

        # Check `price_per_unit` key is in the first dict to confirm its been processed
        self.assertTrue('price_per_unit' in pricing_data[0])
