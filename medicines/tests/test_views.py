'''
Tests for the `medicines` Django web application
'''


from django.test import TestCase
from django.urls import reverse

from medicines import models
from tenders.tests import helpers


class BNFPresentationListViewTests(TestCase):
    '''
    TestCase class for the `BNFPresentationListView` view
    '''

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        helpers.view_test_setup(self)

        self.url_str = reverse('medicines:bnfpresentation-list')

    def test_list_view_anonymous_response(self):
        '''
        `BNFPresentationListView` view should return a redirect response to the login page if
        no-one is logged in
        '''

        response = self.client.get(self.url_str, follow=True)
        # Should redirect to the login page
        redirect_url = '{0}?next={1}'.format(reverse('login'), self.url_str)
        self.assertRedirects(response, redirect_url)

    def test_list_view_user_response(self):
        '''
        `BNFPresentationListView` view should return a standard response if the user is logged in
        indicating success
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(self.url_str)
        self.assertEqual(response.status_code, 200)


class BNFPresentationDetailViewTests(TestCase):
    '''
    TestCase class for the `BNFPresentationDetailView` view
    '''

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        helpers.view_test_setup(self)

        # Create an `BNFPresentationDetail` entry for use with tests
        chemical_substance = models.BNFChemicalSubstance.objects.create(
            code='0407010X0', name='Paracetamol Combined Preparations'
        )
        product = models.BNFProduct.objects.create(
            code='0407010X0CD', name='Boots (Paracet Combined)'
        )

        entry = models.BNFPresentation.objects.create(
            chem_substance=chemical_substance, product=product,
            code='0407010X0CDAFA0', name='Boots_Pharmacy Cold & Flu Day Cap')

        self.url_str = reverse('medicines:bnfpresentation-detail', args=(entry.code, ))

    def test_detail_view_anonymous_response(self):
        '''
        `BNFPresentationDetailView` view should return a redirect response to the login page if
        no-one is logged in
        '''

        response = self.client.get(self.url_str, follow=True)
        # Should redirect to the login page
        redirect_url = '{0}?next={1}'.format(reverse('login'), self.url_str)
        self.assertRedirects(response, redirect_url)

    def test_detail_view_user_response(self):
        '''
        `BNFPresentationDetailView` view should return a standard response if the user is logged
        in indicating success
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(self.url_str)
        self.assertEqual(response.status_code, 200)


class GetPricingDataViewTests(TestCase):
    '''
    TestCase class for the `get_pricing_data` view
    '''

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        helpers.view_test_setup(self)

    def test_view_response_valid_code(self):
        '''
        `get_pricing_data` view should return a json response containing pricing data from the
        Open Prescribing api

        input `code` is a valid code for the Rosuvastatin Calc_Tab 20mg BNF Presentation
        '''

        url_str = reverse('medicines:get-pricing-data', args=('0212000AAAAABAB', ))

        self.client.login(username='jblogs', password='jblogspassword')

        response = self.client.get(url_str)

        # Test that a json packet containing something is returned
        self.assertTrue(response.content.decode('utf8'))

    def test_view_response_invalid_code(self):
        '''
        `get_pricing_data` view should return a json response containing pricing data from the
        Open Prescribing api

        input `code` is a invalid code garbage code
        '''

        url_str = reverse('medicines:get-pricing-data', args=('GARBAGE', ))

        self.client.login(username='jblogs', password='jblogspassword')

        response = self.client.get(url_str)

        # Response should return an empty list for a invalid GARBAGE code
        self.assertJSONEqual(response.content.decode('utf8'), [])
