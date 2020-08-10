'''
Defines custom tags for the `tenders` Django app
'''


from django import template
from django.conf import settings
from django.urls import reverse

from decouple import config


register = template.Library()


@register.simple_tag()
def tedsearch_version():
    '''
    Tag returns version number of tedsearch application

     * If settings.production are in use, returns the value of the `VERSION` Heroku config var.
     * If settings.development are in use, returns "DEV"
    '''

    if settings.SETTINGS_MODULE == 'settings.production':
        # If in production, grab VERSION config var
        return_str = config('VERSION')

    else:
        return_str = 'DEV'

    return return_str


@register.simple_tag()
def contract_award_notice_list_filter(contract_notice):
    '''
    Tag returns a url to show related `contract_award_notice` entries on the
    `ContractAwardNoticeListView` based on the input `contract_notice`. It does this by building a
    string containing the Contract Award Notice `ojs_ref` strings that can then be used in the
    `ojs_ref` in filter
    '''

    # Create a comma separated string containing all the related Contract Award Notice `ojf_ref`
    # strings
    ojs_ref_str = ','.join(
        contract_notice.contractawardnotice_set.values_list('ojs_ref', flat=True)
    )

    # Add this to the `tenders:contractawardnotice-list` url to link to the filtered view
    return reverse('tenders:contractawardnotice-list') + '?ojs_ref=' + ojs_ref_str
