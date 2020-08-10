'''
Tables for the `medicines` Django app
'''


import django_tables2 as tables

from medicines import models


class BNFPresentationTable(tables.Table):
    '''
    Defines the table layout for `BNFPresentation` entries
    '''

    code = tables.Column(linkify=True)

    class Meta:
        attrs = {'class': 'table table-sm'}
        fields = ['code', 'chem_substance', 'product', 'name']
        model = models.BNFPresentation
