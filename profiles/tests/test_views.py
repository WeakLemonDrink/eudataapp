'''
Tests for the `profiles` Django web application
'''


from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from profiles.models import TedSearchTerm
from tenders.tests import helpers


class TedSearchTermCreateViewTests(TestCase):
    '''
    TestCase class for the `TedSearchTermCreateView` view
    '''

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        helpers.view_test_setup(self)

        self.url_str = 'profiles:tedsearchterm-create'
        self.post_data = {'keyword': 'mymedicine', 'send_notifications': 'on'}

    def test_tedsearchterm_create_view_anonymous_response(self):
        '''
        `TedSearchTermCreateView` view should return a redirect response to the login page if
        no-one is logged in
        '''

        response = self.client.get(reverse(self.url_str), follow=True)
        # Should redirect to the login page
        redirect_url = '{0}?next={1}'.format(reverse('login'), reverse(self.url_str))

        self.assertRedirects(response, redirect_url)

    def test_tedsearchterm_create_view_user_response(self):
        '''
        `TedSearchTermCreateView` view should return a standard response if the user is logged in
        indicating success
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))

        self.assertEqual(response.status_code, 200)

    def test_tedsearchterm_create_view_context_contains_app(self):
        '''
        `TedSearchTermCreateView` view should extend the default context to contain `app` for use
        in `tedsearchterm_form.html` template
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))
        self.assertIn('app', response.context)

    def test_tedsearchterm_create_view_context_contains_model_name(self):
        '''
        `TedSearchTermCreateView` view should extend the default context to contain `model_name`
        for use in `tedsearchterm_form.html` template
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))

        self.assertIn('model_name', response.context)

    def test_tedsearchterm_create_view_creates_new_entry(self):
        '''
        `TedSearchTermCreateView` view should create a new `TedSearchTerm` entry if valid data is
        posted
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        self.client.post(reverse(self.url_str), self.post_data)

        # Confirm a new `TedSearchTerm` entry has been created
        self.assertTrue(TedSearchTerm.objects.exists())

    def test_tedsearchterm_create_view_redirects_to_list_view_by_default(self):
        '''
        `TedSearchTermCreateView` view should create a new `TedSearchTerm` entry if valid data is
        posted and redirect to the list view
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.post(reverse(self.url_str), self.post_data)

        # Confirm the response redirects to the list view
        self.assertRedirects(response, reverse('profiles:tedsearchterm-list'))

    def test_tedsearchterm_create_view_redirects_to_add_view_if_requested(self):
        '''
        `TedSearchTermCreateView` view should create a new `TedSearchTerm` entry if valid data is
        posted, and should redirect to the add view again

        the addition of `_addanother` in the post data should redirect to the add view instead of
        list view
        '''

        # Add extra `_addanother` data to `post_data`
        self.post_data['_addanother'] = ''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.post(reverse(self.url_str), self.post_data)

        # Confirm the response redirects to the list view
        self.assertRedirects(response, reverse('profiles:tedsearchterm-create'))

    def test_tedsearchterm_create_view_should_not_allow_multiple_keywords(self):
        '''
        `TedSearchTermCreateView` view should validate inputted keyword data

        If keyword is more than one word, form should error
        '''

        post_data = {'keyword': 'my multiple keyword', 'send_notifications': 'on'}

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.post(reverse(self.url_str), post_data)

        # Confirm the form in the response contains errors linked to the keyword
        self.assertFormError(response, 'form', 'keyword', 'Keyword is not a single word.')

    def test_tedsearchterm_create_view_should_allow_keywords_with_numbers(self):
        '''
        `TedSearchTermCreateView` view should validate inputted keyword data

        If keyword is a single word, but contains both characters and numbers form should not
        error and create a new `TedSearchTerm` entry
        '''

        post_data = {'keyword': 'medicines1212', 'send_notifications': 'on'}

        self.client.login(username='jblogs', password='jblogspassword')
        self.client.post(reverse(self.url_str), post_data)

        # Confirm a new `TedSearchTerm` entry has been created
        self.assertTrue(TedSearchTerm.objects.exists())


class TedSearchTermListViewTests(TestCase):
    '''
    TestCase class for the `TedSearchTermListView` view
    '''

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        helpers.view_test_setup(self)

        self.url_str = 'profiles:tedsearchterm-list'

    def test_tedsearchterm_list_view_anonymous_response(self):
        '''
        `TedSearchTermListView` view should return a redirect response to the login page if no-one
        is logged in
        '''

        response = self.client.get(reverse(self.url_str), follow=True)
        # Should redirect to the login page
        redirect_url = '{0}?next={1}'.format(reverse('login'), reverse(self.url_str))

        self.assertRedirects(response, redirect_url)

    def test_tedsearchterm_list_view_user_response(self):
        '''
        `TedSearchTermListView` view should return a standard response if the user is logged in
        indicating success
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))

        self.assertEqual(response.status_code, 200)

    def test_tedsearchterm_list_view_context_contains_app(self):
        '''
        `TedSearchTermListView` view should extend the default context to contain `app` for
        use in `list.html` template
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))

        self.assertTrue('app' in response.context)

    def test_tedsearchterm_list_view_context_contains_model_name(self):
        '''
        `TedSearchTermListView` view should extend the default context to contain `model_name` for
        use in `list.html` template
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))

        self.assertTrue('model_name' in response.context)

    def test_tedsearchterm_list_view_filters_queryset_correctly(self):
        '''
        `TedSearchTermListView` view should only list `TedSearchTerm` entries that have a `user`
        ForeignKey linked to the user logged in to the current session
        '''

        # Create some `TedSearchTerm` entries linked to the jbloggs user
        TedSearchTerm.objects.create(user=self.user, keyword='mymedicine1')
        TedSearchTerm.objects.create(user=self.user, keyword='mymedicine2')

        # Create some `TedSearchTerm` entries linked to another user
        another_user = User.objects.create(username='jsnow')
        TedSearchTerm.objects.create(user=another_user, keyword='mymedicine1')
        TedSearchTerm.objects.create(user=another_user, keyword='mymedicine2')
        TedSearchTerm.objects.create(user=another_user, keyword='mymedicine3')

        # Login as jbloggs
        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))
        queryset = response.context['tedsearchterm_list']

        # Returned queryset should contain 2 entries linked to jbloggs only
        self.assertEqual(queryset.count(), 2)


class DashboardViewTests(TestCase):
    '''
    TestCase class for the `dashboard` method view
    '''

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        helpers.view_test_setup(self)

        self.url_str = 'profiles:dashboard'

    def test_dashboard_view_anonymous_response(self):
        '''
        `dashboard` view should return a redirect response to the login page if no-one is logged in
        '''

        response = self.client.get(reverse(self.url_str), follow=True)
        # Should redirect to the login page
        redirect_url = '{0}?next={1}'.format(reverse('login'), reverse(self.url_str))

        self.assertRedirects(response, redirect_url)

    def test_dashboard_list_view_user_response(self):
        '''
        `dashboard` view should return a standard response if the user is logged in indicating
        success
        '''

        self.client.login(username='jblogs', password='jblogspassword')
        response = self.client.get(reverse(self.url_str))

        self.assertEqual(response.status_code, 200)
   