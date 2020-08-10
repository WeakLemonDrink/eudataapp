'''
Tables for the `profiles` Django app
'''


import django_tables2 as tables

from profiles import models


class TedSearchTermTable(tables.Table):
    '''
    Defines the table layout for `TedSearchTerm` entries
    '''

    options = tables.TemplateColumn(
        template_name='profiles/tedsearchterm_list_options.html', verbose_name=''
    )

    class Meta:
        attrs = {'class': 'table table-sm'}
        fields = ['keyword', 'send_notifications', 'is_active', 'options']
        model = models.TedSearchTerm
