'''
Filters for the `medicines` Django app
'''


from django.db.models import Q
from django.forms import widgets

import django_filters as filters

from medicines import models


class BNFPresentationFilter(filters.FilterSet):
    '''
    Defines the filterset for `BNFPresentation` entries
    '''

    BOOLEAN_CHOICES = ((True, 'Yes'), (False, 'No'))

    is_generic = filters.ChoiceFilter(
        choices=BOOLEAN_CHOICES, empty_label='All', field_name='product__is_generic',
        label='Generic?'
    )
    search = filters.CharFilter(
        label='Search', method='search_method',
        widget=widgets.TextInput(
            attrs={
                'data-toggle': 'tooltip',
                'data-placement': 'top',
                'title': 'Search presentation name, product, chemical substance or BNF code'
            }
        )
    )

    def search_method(self, queryset, name, value):
        '''Provides a method to search across the following fields using `Q` methods:
         * name
         * product__name
         * chem_substance__name
         * code
        '''

        return queryset.filter(
            Q(name__icontains=value) | Q(product__name__icontains=value) |
            Q(chem_substance__name__icontains=value) | Q(code__icontains=value)
        )

    class Meta:
        fields = ['search', 'is_generic']
        model = models.BNFPresentation
