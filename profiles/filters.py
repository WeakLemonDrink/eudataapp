'''
Filters for the `profiles` Django app
'''


import datetime

import django_filters as filters

from profiles import models
from tenders.models import ContractNotice


def truncate(dt):
    '''
    Method truncates a datetime object to a date
    '''

    return dt.date()


class DashboardPublicationDateFilter(filters.FilterSet):
    '''
    Defines a filter for `ContractNotice` entries `publication_date` field
    '''

    publication_date = filters.CharFilter(method='filter_publication_date')

    def filter_publication_date(self, queryset, name, value):
        '''
        Custom filter method so we can accept either a single integer to filter by a date range,
        or a single date string

        If the value is not a date string, or an integer just return the unfiltered queryset
        '''

        # First, check whether the input value is a date
        try:
            single_date = datetime.datetime.strptime(value, '%d/%m/%Y')

            filtered_qs = queryset.filter(**{name: single_date})

        except ValueError:
            # If its not a date string, then maybe its a number that we should use to filter by
            # range
            if value in ['7', '14', '21']:

                now = datetime.datetime.now()

                filtered_qs = queryset.filter(**{
                    '%s__gte' % name: truncate(now - datetime.timedelta(days=int(value))),
                    '%s__lt' % name: truncate(now + datetime.timedelta(days=1)),
                })

            else:
                # Return unfiltered qs by default
                filtered_qs = queryset

        return filtered_qs

    class Meta:
        fields = ['publication_date']
        models = ContractNotice


class TedSearchTermFilter(filters.FilterSet):
    '''
    Defines the filterset for `TedSearchTerm` entries
    '''

    BOOLEAN_CHOICES = ((True, 'Yes'), (False, 'No'))

    is_active = filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES, empty_label='All', label='Is active?'
    )
    send_notifications = filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES, empty_label='All', label='Send notifications?'
    )

    class Meta:
        fields = ['send_notifications', 'is_active']
        model = models.TedSearchTerm
