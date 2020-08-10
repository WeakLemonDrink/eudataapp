'''
Tables for the `tenders` Django app
'''


import django_tables2 as tables

from tenders import models


class CommaSeparatorColumn(tables.Column):
    '''
    Custom column that inserts comma separators to integers or decimals for easier readability
    e.g. 1,000,000.00
    '''

    def render(self, value):
        '''
        Render the value with comma separators
        '''

        return '{:,}'.format(value)


class ContractNoticeTable(tables.Table):
    '''
    Defines the table layout for `ContractNotice` entries
    '''

    closing_date = tables.DateColumn(format='d/m/Y')
    ojs_ref = tables.TemplateColumn(
        '<a href="{{record.url}}" target="_blank">{{record.ojs_ref}}</a>'
    )
    procurement_docs_url = tables.TemplateColumn(
        template_name='tenders/procurement_docs_url_truncated_text.html'
    )
    options = tables.TemplateColumn(
        template_name='tenders/contract_notice_list_options.html', verbose_name=''
    )

    class Meta:
        attrs = {'class': 'table table-sm'}
        fields = ['id', 'ojs_ref', 'title', 'procurement_docs_url', 'contracting_body_name',
                  'country', 'publication_date', 'closing_date', 'options']
        model = models.ContractNotice
        order_by = ['-publication_date', '-closing_date']


class ContractAwardNoticeTable(tables.Table):
    '''
    Defines the table layout for `ContractAwardNotice` entries
    '''

    dispatch_date = tables.DateColumn(format='d/m/Y')
    ojs_ref = tables.TemplateColumn(
        '<a href="{{record.url}}" target="_blank">{{record.ojs_ref}}</a>'
    )
    options = tables.TemplateColumn(
        template_name='tenders/contract_award_notice_list_options.html', verbose_name=''
    )
    value_of_procurement = CommaSeparatorColumn()

    class Meta:
        attrs = {'class': 'table table-sm'}
        fields = ['id', 'ojs_ref', 'title', 'contracting_body_name', 'country', 'dispatch_date',
                  'value_of_procurement', 'currency', 'options']
        model = models.ContractAwardNotice
        order_by_field = 'ordering'


class LotTable(tables.Table):
    '''
    Defines the table layout for `Lot` entries
    '''

    contract_notice = tables.TemplateColumn(
        '<a href="{{record.contract_notice.url}}" ' +
        'target="_blank">{{record.contract_notice}}</a>'
    )
    info_add = tables.TemplateColumn(template_name='tenders/lot_list_truncated_text.html')
    short_descr = tables.TemplateColumn(template_name='tenders/lot_list_truncated_text.html')
    title = tables.TemplateColumn(template_name='tenders/lot_list_truncated_text.html')
    conclusion_date = tables.DateColumn(format='d/m/Y')
    value = CommaSeparatorColumn()
    value_per_unit = CommaSeparatorColumn()

    class Meta:
        attrs = {'class': 'table table-sm table'}
        fields = ['contract_notice', 'lot_no', 'title', 'short_descr', 'info_add',
                  'awarded_contract', 'conclusion_date', 'contractor_name', 'contractor_country',
                  'value', 'number_of_units', 'value_per_unit', 'currency']
        model = models.Lot
        order_by_field = 'ordering'
