'''
Tests for the `tenders` Django web application
'''


from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from tenders import models
from tenders.tests import helpers


class LotListViewTests(TestCase):
    '''
    TestCase class for the `LotListView` view
    '''

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        helpers.view_test_setup(self)

        self.url_str = 'tenders:lot-list'

    def test_lot_list_view_anonymous_response(self):
        '''
        `LotListView` view should return a redirect response to the login page if no-one is logged
        in
        '''

        response = self.client.get(reverse(self.url_str), follow=True)
        # Should redirect to the login page
        redirect_url = '{0}?next={1}'.format(reverse('login'), reverse(self.url_str))
        self.assertRedirects(response, redirect_url)

    def test_lot_list_view_user_response(self):
        '''
        `LotListView` view should return a standard response if the user is logged in
        indicating success
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))
        self.assertEqual(response.status_code, 200)

    def test_lot_list_view_context_contains_model_name(self):
        '''
        `LotListView` view should extend the default context to contain `model_name` for use
        in `list.html` template
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))
        self.assertTrue('model_name' in response.context)


class TenderBulkCreateViewTests(TestCase):
    '''
    TestCase class for the `TenderBulkCreateView` view
    '''

    fixtures = [
        './files/initial_data/countries.xml',
        './files/initial_data/currencies.xml'
    ]

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        helpers.view_test_setup(self)

        self.url_str = 'tenders:tender-bulk-create'

    def test_tender_bulk_create_view_anonymous_response(self):
        '''
        `TenderBulkCreateView` view should return a redirect response to the login page if
        no-one is logged in
        '''

        response = self.client.get(reverse(self.url_str), follow=True)
        # Should redirect to the login page
        redirect_url = '{0}?next={1}'.format(reverse('login'), reverse(self.url_str))
        self.assertRedirects(response, redirect_url)

    def test_tender_bulk_create_view_user_response(self):
        '''
        `TenderBulkCreateView` view should return a standard response if the user is logged in
        indicating success
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_tender_bulk_create_view_upload_invalid_file_raises_error(self):
        '''
        `TenderBulkCreateView` view should raise errors via the `UploadBulkDataForm` form when
        invalid data is uploaded

        If the date entered does not have an associated daily package file on the ftp server, an
        error should be raised attached to the `date` field
        '''

        # Create the post data. Date is a weekend so should not have an associated daily package
        # file on the ftp server
        post_data = {'date': '21/09/2019'}

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.post(reverse(self.url_str), post_data)

        # Grab the returned form
        form = response.context['form']

        # Unsuccessful upload of file should raise errors
        self.assertTrue(form.errors)


class TenderSingleCreateViewTests(TestCase):
    '''
    TestCase class for the `TenderSingleCreateView` view
    '''

    fixtures = [
        './files/initial_data/countries.xml',
        './files/initial_data/currencies.xml'
    ]

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        helpers.view_test_setup(self)

        self.url_str = 'tenders:tender-create'

    def test_tender_single_create_view_anonymous_response(self):
        '''
        `TenderSingleCreateView` view should return a redirect response to the login page if
        no-one is logged in
        '''

        response = self.client.get(reverse(self.url_str), follow=True)
        # Should redirect to the login page
        redirect_url = '{0}?next={1}'.format(reverse('login'), reverse(self.url_str))
        self.assertRedirects(response, redirect_url)

    def test_tender_single_create_view_user_response(self):
        '''
        `TenderSingleCreateView` view should return a standard response if the user is logged in
        indicating success
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_tender_single_create_view_upload_valid_f02_file_redirects(self):
        '''
        `TenderSingleCreateView` view should create new `ContractNotice` entry via the
        `UploadXmlFileForm` form when valid data is uploaded

        TED F02 export file 2019-OJS156-384676.xml is valid cpv code, document type and contract
        type

        Successful upload of file should redirect to the `ContractNotice` list view
        '''

        # Create the upload file. File is a valid TED export correct data
        upload_file = helpers.create_files_data('2019-OJS156-384676.xml', settings.TEST_FILES_DIR)

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.post(reverse(self.url_str), upload_file, follow=True)

        # Successful upload of file should redirect to the `ContractNotice` list view
        self.assertRedirects(response, reverse('tenders:contractnotice-list'))

    def test_tender_single_create_view_upload_valid_f02_file_creates_entry(self):
        '''
        `TenderSingleCreateView` view should create new `ContractNotice` entry via the
        `UploadXmlFileForm` form when valid data is uploaded

        TED F02 export file 2019-OJS156-384676.xml is valid cpv code, document type and contract
        type

        Successful upload of file should create new `ContractNotice` entry
        '''


        # Create the upload file. File is a valid TED export correct data
        upload_file = helpers.create_files_data('2019-OJS156-384676.xml', settings.TEST_FILES_DIR)

        self.client.login(username='jblogs', password='jblogspassword')
        self.client.post(reverse(self.url_str), upload_file)

        # Successful upload of file should have created a new `ContractNotice` entry
        self.assertTrue(models.ContractNotice.objects.exists())

    def test_tender_single_create_view_upload_valid_f03_file_redirects(self):
        '''
        `TenderSingleCreateView` view should create new `ContractAwardNotice` entry via the
        `UploadXmlFileForm` form when valid data is uploaded

        TED F03 export file 2019-OJS097-234233.xml is valid cpv code, document type and contract
        type

        Successful upload of file should redirect to the `ContractAwardNotice` list view
        '''

        # Upload file needs a corresponding contract notice to for view to work
        # Load 2018/S 244-557823 and associated lots from fixture
        helpers.load_fixtures(self, 'test_tender_single_create_view_upload_valid_f03_file.xml')

        # Create the upload file. File is a valid TED export correct data
        upload_file = helpers.create_files_data('2019-OJS097-234233.xml', settings.TEST_FILES_DIR)

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.post(reverse(self.url_str), upload_file, follow=True)

        # Successful upload of file should redirect to the `ContractAwardNotice` list view
        self.assertRedirects(response, reverse('tenders:contractawardnotice-list'))

    def test_tender_single_create_view_upload_valid_f03_file_creates_entry(self):
        '''
        `TenderSingleCreateView` view should create new `ContractAwardNotice` entry via the
        `ImportXmlFile` form when valid data is uploaded

        TED F03 export file 2019-OJS097-234233.xml is valid cpv code, document type and contract
        type

        Successful upload of file should create new `ContractAwardNotice` entry
        '''

        # Upload file needs a corresponding contract notice to for view to work
        # Load 2018/S 244-557823 and associated lots from fixture
        helpers.load_fixtures(self, 'test_tender_single_create_view_upload_valid_f03_file.xml')

        # Create the upload file. File is a valid TED export correct data
        upload_file = helpers.create_files_data('2019-OJS097-234233.xml', settings.TEST_FILES_DIR)

        self.client.login(username='jblogs', password='jblogspassword')
        self.client.post(reverse(self.url_str), upload_file)

        # Successful upload of file should have created a new `ContractAwardNotice` entry
        self.assertTrue(models.ContractAwardNotice.objects.exists())


class ContactNoticeListViewTests(TestCase):
    '''
    TestCase class for the `ContactNoticeListView` view
    '''

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        helpers.view_test_setup(self)

        self.url_str = 'tenders:contractnotice-list'

    def test_tender_list_view_anonymous_response(self):
        '''
        `ContactNoticeListView` view should return a redirect response to the login page if
        no-one is logged in
        '''

        response = self.client.get(reverse(self.url_str), follow=True)
        # Should redirect to the login page
        redirect_url = '{0}?next={1}'.format(reverse('login'), reverse(self.url_str))
        self.assertRedirects(response, redirect_url)

    def test_tender_list_view_user_response(self):
        '''
        `ContactNoticeListView` view should return a standard response if the user is logged in
        indicating success
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_lot_list_view_context_contains_model_name(self):
        '''
        `ContactNoticeListView` view should extend the default context to contain `model_name` for
        use in `list.html` template
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))
        self.assertTrue('model_name' in response.context)


class SignS3ViewTests(TestCase):
    '''
    blah
    '''

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        helpers.view_test_setup(self)

        self.url_str = 'tenders:sign-s3'

    def test_sign_s3_view_post_anonymous_response(self):
        '''
        `sign_s3` view should return a redirect response to the login page if no-one is
        logged in
        '''

        response = self.client.post(reverse(self.url_str), follow=True)
        # Should redirect to the login page
        redirect_url = '{0}?next={1}'.format(reverse('login'), reverse(self.url_str))
        self.assertRedirects(response, redirect_url)

    def test_sign_s3_view_post_valid_data(self):
        '''
        `sign_s3` view should return a json response including data ready to be used for file
        upload to s3
        '''

        get_data = {'file_name': '20190719_2019138.tar.gz', 'file_type': 'tar.gz'}

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str), get_data)

        # Confirm the response contains something
        self.assertTrue(response)
