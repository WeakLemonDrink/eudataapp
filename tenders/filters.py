'''
Filters for the `tenders` Django app
'''


import django_filters as filters

from profiles.models import TedSearchTerm
from tenders import models


class ContractNoticeFilter(filters.FilterSet):
    '''
    Defines the filterset for `ContractNotice` entries
    '''

    country = filters.ModelChoiceFilter(
        queryset=models.Country.objects.filter(is_active=True)
    )
    closing_date = filters.DateFromToRangeFilter(
        help_text='From - To Date Range',
        widget=filters.widgets.DateRangeWidget(
            attrs={
                'data-provide': 'datepicker',
                'data-date-format': 'dd/mm/yyyy'
            }
        )
    )
    publication_date = filters.DateRangeFilter()
    lot__search_vector = filters.ChoiceFilter(label='My Search Terms', lookup_expr='icontains')

    def __init__(self, *args, **kwargs):
        '''
        Override default `__init__` to deal with extra incoming `user` kwarg
        '''

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        # Use input `user` to contruct search term choices from `TedSearchTerm` entries
        search_term_qs = TedSearchTerm.objects.filter(user=user)

        if search_term_qs.exists():
            # Update the choices to the search terms linked to the user
            self.filters['lot__search_vector'].extra['choices'] = (
                (e.keyword, str(e)) for e in search_term_qs
            )

        else:
            # Disable the filter as it won't do anything
            self.filters['lot__search_vector'].extra['disabled'] = True

    class Meta:
        fields = ['ojs_ref', 'country', 'closing_date', 'publication_date', 'lot__search_vector']
        model = models.ContractNotice


class LotFilter(filters.FilterSet):
    '''
    Defines the filterset for `Lot` entries
    '''

    BOOLEAN_CHOICES = ((True, 'Yes'), (False, 'No'))

    awarded_contract = filters.ChoiceFilter(choices=BOOLEAN_CHOICES, empty_label='All')
    contractor_country = filters.ModelChoiceFilter(
        queryset=models.Country.objects.filter(is_active=True)
    )
    conclusion_date = filters.DateFromToRangeFilter(
        widget=filters.widgets.DateRangeWidget(
            attrs={
                'data-provide': 'datepicker',
                'data-date-format': 'dd/mm/yyyy'
            }
        )
    )
    currency = filters.ModelChoiceFilter(
        queryset=models.Currency.objects.filter(is_active=True)
    )
    # search_vector is set to search in `title`, `short_descr` and `info_add` by
    # `tasks.tasks.update_lot_search_vector`
    search_vector = filters.CharFilter(label='Search', lookup_expr='icontains')

    class Meta:
        fields = ['contract_notice', 'awarded_contract', 'conclusion_date',
                  'contractor_country', 'currency', 'search_vector']
        model = models.Lot


class OjsRefInFilter(filters.BaseInFilter, filters.CharFilter):
    '''
    Defines a filter to allow us to filter using the `__in` lookup
    '''


class ContractAwardNoticeFilter(filters.FilterSet):
    '''
    Defines the filterset for `ContractAwardNotice` entries
    '''

    ojs_ref = OjsRefInFilter(label='OJS Reference', lookup_expr='in')
    country = filters.ModelChoiceFilter(
        queryset=models.Country.objects.filter(is_active=True)
    )
    currency = filters.ModelChoiceFilter(
        queryset=models.Currency.objects.filter(is_active=True)
    )
    dispatch_date = filters.DateFromToRangeFilter(
        help_text='From - To Date Range',
        widget=filters.widgets.DateRangeWidget(
            attrs={
                'data-provide': 'datepicker',
                'data-date-format': 'dd/mm/yyyy'
            }
        )
    )

    class Meta:
        fields = ['ojs_ref', 'country', 'dispatch_date', 'currency']
        model = models.ContractAwardNotice
