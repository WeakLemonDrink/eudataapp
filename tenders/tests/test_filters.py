'''
Tests for `tenders.filters` in the `tenders` Django web application
'''


from django.contrib.auth.models import User
from django.test import TestCase

from profiles.models import TedSearchTerm
from tenders.filters import ContractNoticeFilter


class ContractNoticeFilterTests(TestCase):
    '''
    TestCase class for the `ContractNoticeFilter` filter
    '''

    def setUp(self):
        '''
        Common setup across methods
        '''

        self.user = User.objects.create_user('jblogs', 'joseph.blogs@django.com', 'jblogspassword')

    def test_filter_init_without_user(self):
        '''
        `ContractNoticeFilter` `__init__` method should work correctly without error if a `user`
        kwarg is not supplied
        '''

        cn_filter = ContractNoticeFilter()

        self.assertTrue(cn_filter)

    def test_filter_init_with_user(self):
        '''
        `ContractNoticeFilter` `__init__` method should work correctly without error if a `user`
        kwarg is supplied
        '''

        cn_filter = ContractNoticeFilter(user=self.user)

        self.assertTrue(cn_filter)

    def test_filter_init_with_user_no_search_terms_lot__search_vector_disabled(self):
        '''
        `ContractNoticeFilter` `__init__` method should work correctly without error if a `user`
        kwarg is supplied

        `lot__search_vector` filter should be disabled if input `user` has no associated
        `TedSearchTerm` entries
        '''

        cn_filter = ContractNoticeFilter(user=self.user)

        self.assertTrue(cn_filter.filters['lot__search_vector'].extra['disabled'])

    def test_filter_init_with_user_no_search_terms_lot__search_vector_no_choices(self):
        '''
        `ContractNoticeFilter` `__init__` method should work correctly without error if a `user`
        kwarg is supplied

        `lot__search_vector` filter should have no choices set if `user` has no associated
        `TedSearchTerm` entries
        '''

        cn_filter = ContractNoticeFilter(user=self.user)

        self.assertIsNone(cn_filter.filters['lot__search_vector'].extra.get('choices', None))

    def test_filter_init_with_user_search_terms_lot__search_vector_enabled(self):
        '''
        `ContractNoticeFilter` `__init__` method should work correctly without error if a `user`
        kwarg is supplied

        `lot__search_vector` filter should not have a `disabled` attribute if input `user` has
        associated `TedSearchTerm` entries
        '''

        # Create some dummy `TedSearchTerm` entries linked to the user
        TedSearchTerm.objects.create(user=self.user, keyword='mymed1')
        TedSearchTerm.objects.create(user=self.user, keyword='mymed2')
        TedSearchTerm.objects.create(user=self.user, keyword='mymed3')

        cn_filter = ContractNoticeFilter(user=self.user)

        self.assertIsNone(cn_filter.filters['lot__search_vector'].extra.get('disabled', None))

    def test_filter_init_with_user_search_terms_lot__search_vector_choices(self):
        '''
        `ContractNoticeFilter` `__init__` method should work correctly without error if a `user`
        kwarg is supplied

        `lot__search_vector` filter should have choices set if `user` has associated
        `TedSearchTerm` entries
        '''

        # Create some dummy `TedSearchTerm` entries linked to the user
        TedSearchTerm.objects.create(user=self.user, keyword='mymed1')
        TedSearchTerm.objects.create(user=self.user, keyword='mymed2')
        TedSearchTerm.objects.create(user=self.user, keyword='mymed3')

        cn_filter = ContractNoticeFilter(user=self.user)

        self.assertTrue(cn_filter.filters['lot__search_vector'].extra['choices'])
