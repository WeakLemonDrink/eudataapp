'''
Tests for `portfolio.models` in the `portfolio` Django web application
'''


from django.contrib.auth.models import User
from django.test import TestCase

from profiles.models import TedSearchTerm


class TedSearchTermModelTests(TestCase):
    '''
    TestCase class for the `TedSearchTerm` model
    '''

    def setUp(self):
        '''
        Common setup
        '''

        self.user = User.objects.create(username='joesproggs')

    def test_str_method_return_correct_string(self):
        '''
        `TedSearchTerm` model entry `__str__()` method should return the `keyword`
        '''

        keyword = 'mymedicine'

        new_entry = TedSearchTerm.objects.create(user=self.user, keyword=keyword)

        self.assertEqual(str(new_entry), keyword)

    def test_save_method_sets_keyword_to_lower_case(self):
        '''
        `TedSearchTerm` model entry `save()` method should set the inputted `keyword` to lower
        case so it is better to use for searching
        '''

        keyword = 'MyMEDicine'

        new_entry = TedSearchTerm.objects.create(user=self.user, keyword=keyword)

        self.assertEqual(new_entry.keyword, 'mymedicine')
