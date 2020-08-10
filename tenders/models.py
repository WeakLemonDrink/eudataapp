'''
Models for the `tenders` Django app
'''


import os
import re

from django.db import models
from django.conf import settings
from django.contrib.postgres.search import SearchVectorField
from django.dispatch import receiver


def concatenate_list_of_strings(input_obj):
    '''
    Function concatenates `input_obj` into one string with newline characters if it is a list

     * If `input_obj` is a list, concatenate the elements into one string with newline characters
       and return
     * If `input_obj` is not a list, return `input_obj` unmodified
    '''

    if isinstance(input_obj, list):
        return_str = '\n'.join(input_obj)

    else:
        # If no match, just return the unmodified `input_obj`
        return_str = input_obj

    return return_str


def contract_notice_file_path(instance, filename):
    '''
    Method can be called from `ContractNotice.procurement_docs_file` `upload_to` argument to set
    the file path for an uploaded file on AWS S3
    '''

    return os.path.join(
        instance._meta.app_label, instance._meta.model_name, str(instance.id), filename
    )


def update_url_language_tab(url):
    '''
    Returns an updated url replacing the language tab (e.g. 'PL') with 'EN' if it exists. This
    ensures the page at the given url will be in English when clicked

    If the regex matches, `url` is updated with 'EN' language tab and returned as `return_url`
    If the regex doesn't match, `url` is returned unmodified
    '''

    match = re.search(r'TEXT:(?P<lang_tag>\D{2}):HTML$', url)

    if match:
        # Update `url` with 'EN' language tag
        # Use the colons either side to make sure we don't replace the wrong part
        find_str = ':' + match.group('lang_tag') + ':'
        replace_str = ':' + settings.TED_EXPORT_LANG_STR + ':'

        return_url = url.replace(find_str, replace_str)

    else:
        # If no match, just return the unmodified `url`
        return_url = url

    return return_url


class Country(models.Model):
    '''
    Defines database table structure for `Country` entries

    List of all possible ISO 3166 alpha-2 country codes and their corresponding name string
     * https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
     * ./files/ted_schema/R2_0_9_S03_E01/countries.xsd

    `is_active` field can be used to remove countries from the admin if they are not relevant
    '''

    iso_code = models.CharField('ISO Code', max_length=2, unique=True)
    country_name = models.CharField('Country Name', max_length=140)
    is_active = models.BooleanField(default=False)

    class Meta:
        app_label = 'tenders'
        ordering = ['iso_code']
        verbose_name_plural = 'Countries'

    def set_is_active(self):
        '''
        Method sets 'is_active' to `True` and saves if `is_active` is `False.

        Setting `is_active` to `True` will ensure we can filter entries to only show ones we care
        about
        '''

        if not self.is_active:
            self.is_active = True
            self.save()

    def __str__(self):
        '''
        Defines the return string for an `Country` entry
        '''

        return '{} {}'.format(self.iso_code, self.country_name)


class Currency(models.Model):
    '''
    Defines database table structure for `Currency` entries

    List of all possible ISO 4217 currency codes and their corresponding name string
     * https://en.wikipedia.org/wiki/ISO_4217

    `is_active` field can be used to remove currencies from the admin if they are not relevant
    '''

    iso_code = models.CharField('ISO Code', max_length=3, unique=True)
    currency_name = models.CharField('Currency Name', max_length=140)
    is_active = models.BooleanField(default=False)

    class Meta:
        app_label = 'tenders'
        ordering = ['iso_code']
        verbose_name_plural = 'Currencies'

    def set_is_active(self):
        '''
        Method sets 'is_active' to `True` and saves if `is_active` is `False.

        Setting `is_active` to `True` will ensure we can filter entries to only show ones we care
        about
        '''

        if not self.is_active:
            self.is_active = True
            self.save()

    def __str__(self):
        '''
        Defines the return string for an `Currency` entry
        '''

        return '{} {}'.format(self.iso_code, self.currency_name)


class ContractNotice(models.Model):
    '''
    Defines database table structure for `ContractNotice` entries

    This table contains data linked to TED Contract Notices, form F02
    '''

    added_timestamp = models.DateTimeField('Added to Database Timestamp', auto_now_add=True)
    # in the format 9999/S 999-999999
    ojs_ref = models.CharField('OJS Reference', max_length=17, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=700)
    short_descr = models.TextField('Short Description')
    contracting_body_name = models.CharField('Contracting Body Name', max_length=400)
    closing_date = models.DateTimeField('Closing Date')
    dispatch_date = models.DateField('Dispatch Date')
    publication_date = models.DateField('Publication Date')
    procurement_ref = models.CharField('Procurement Reference', max_length=140, null=True,
                                       blank=True)
    procurement_docs_url = models.URLField('Procurement Documents Location')
    full_docs_available = models.BooleanField(default=True)
    procurement_docs_file = models.FileField(
        'Procurement Document File', upload_to=contract_notice_file_path, null=True, blank=True
    )

    class Meta:
        app_label = 'tenders'
        ordering = ['ojs_ref']
        verbose_name = 'Contract Notice'

    def save(self, *args, **kwargs):
        '''
        Override default save to:
         * Modify url to include the 'EN' language tab using `update_url_language_tab`
         * Call `Country` ForeignKey `set_is_active`
         * If `short_descr` is list, concatenate using `concatenate_list_of_strings`
         * If `procurement_docs_url` doesn't start with http, add this to make sure it's not
           treated as a relative url when displaying in future
        '''

        # Only do on initial save
        if self.pk is None:
            # Modify `self.url`
            self.url = update_url_language_tab(self.url)

            # Update `Country` and `Currency` ForeignKeys
            self.country.set_is_active()

            # If a list is provided to `short_descr`, concatenate list elements with newlines
            self.short_descr = concatenate_list_of_strings(self.short_descr)

            # Modify `self.procurement_docs_url`
            if not self.procurement_docs_url.startswith('http'):
                self.procurement_docs_url = 'http://' + self.procurement_docs_url

        # Call default save
        super().save(*args, **kwargs)


    def __str__(self):
        '''
        Defines the return string for a `ContractNotice` entry
        '''

        return self.ojs_ref


@receiver(models.signals.pre_save, sender=ContractNotice)
def auto_delete_procurement_docs_file_on_change(sender, instance, **kwargs):
    '''
    Deletes old file from filesystem when corresponding `ContractNotice` object is updated with new
    file at `procurement_docs_file` field

    Only do this when an object already exists (not initial save) and when the
    pre save entry `procurement_docs_file` field is filled
    '''

    # Don't check on initial save or if we're loading from fixtures
    if instance.pk and not kwargs.get('raw', False):
        old_file = sender.objects.get(pk=instance.pk).procurement_docs_file

        # Only check if an old file exists
        if old_file:
            # If the file has changed, delete the old file before the new one is saved
            if not old_file == instance.procurement_docs_file:
                old_file.delete(save=False)


class ContractAwardNotice(models.Model):
    '''
    Defines database table structure for `ContractAwardNotice` entries
    '''

    added_timestamp = models.DateTimeField('Added to Database Timestamp', auto_now_add=True)
    # in the format 9999/S 999-999999
    ojs_ref = models.CharField('OJS Reference', max_length=17, unique=True)
    contract_notice = models.ForeignKey(ContractNotice, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=700)
    short_descr = models.TextField('Short Description')
    contracting_body_name = models.CharField('Contracting Body Name', max_length=400)
    dispatch_date = models.DateField('Dispatch Date')
    publication_date = models.DateField('Publication Date')
    length_of_tender = models.DurationField('Length of Tender', null=True, blank=True)
    value_of_procurement = models.DecimalField('Value of Procurement', max_digits=15,
                                               decimal_places=2, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        app_label = 'tenders'
        ordering = ['ojs_ref']
        verbose_name = 'Contract Award Notice'

    def save(self, *args, **kwargs):
        '''
        Override default save to:
         * Modify url to include the 'EN' language tab
         * Call `Country` and `Currency` ForeignKeys `set_is_active`
         * If `short_descr` is list, concatenate with newlines
        '''

        # Only do on initial save
        if self.pk is None:
            # Modify `self.url`
            self.url = update_url_language_tab(self.url)

            # Update `Country` and `Currency` ForeignKeys
            self.country.set_is_active()

            if self.currency:
                self.currency.set_is_active()

            # If a list is provided to `short_descr`, concatenate list elements with newlines
            self.short_descr = concatenate_list_of_strings(self.short_descr)

        # Call default save
        super().save(*args, **kwargs)

    def __str__(self):
        '''
        Defines the return string for a `Tender` entry
        '''

        return self.ojs_ref


class Lot(models.Model):
    '''
    Defines database table structure for `Lot` entries
    '''

    added_timestamp = models.DateTimeField('Added to Database Timestamp', auto_now_add=True)
    contract_notice = models.ForeignKey(ContractNotice, on_delete=models.CASCADE,
                                        verbose_name='Contract Notice')
    lot_no = models.PositiveIntegerField('Lot No.')
    awarded_contract = models.BooleanField('Awarded Contract', default=False)
    title = models.CharField(max_length=400)
    short_descr = models.TextField('Short Description', null=True, blank=True)
    info_add = models.TextField('Additional Information', null=True, blank=True)
    conclusion_date = models.DateField('Conclusion Date', null=True, blank=True)
    contractor_name = models.CharField('Contractor Name', max_length=400, null=True, blank=True)
    contractor_country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name='Contractor Country',
        null=True, blank=True
    )
    awarded_to_group = models.BooleanField('Awarded To Group', default=False)
    value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    value_estimated = models.BooleanField(default=False)
    number_of_units = models.PositiveIntegerField('Number of Units', null=True, blank=True)
    value_per_unit = models.DecimalField('Value per Unit', max_digits=15, decimal_places=2,
                                         null=True, blank=True)
    search_vector = SearchVectorField(null=True, editable=False)

    class Meta:
        app_label = 'tenders'
        ordering = ['contract_notice', 'lot_no']

    def save(self, *args, **kwargs):
        '''
        Override default save to:

         * `Country` and `Currency` ForeignKeys `set_is_active`
         * If `info_add` is list, concatenate with newlines
         * If `short_descr` is list, concatenate with newlines
         * If `value` and `number_of_units` are filled, calculate `value_per_unit`
        '''

        # Only do on initial save
        if self.pk is None:
            # Update `Country` and `Currency` ForeignKeys
            if self.contractor_country is not None:
                self.contractor_country.set_is_active()

            if self.currency is not None:
                self.currency.set_is_active()

            # If a list is provided to `info_add`, concatenate list elements with newlines
            self.info_add = concatenate_list_of_strings(self.info_add)

            # If a list is provided to `short_descr`, concatenate list elements with newlines
            self.short_descr = concatenate_list_of_strings(self.short_descr)

        # Calculate `value_per_unit` if data is available
        if self.number_of_units and self.value:
            self.value_per_unit = self.value / self.number_of_units

        else:
            # If both are not present, clear `value_per_unit`
            self.value_per_unit = None

        # Call default save
        super().save(*args, **kwargs)

    def __str__(self):
        '''
        Defines the return string for a `Lot` entry
        '''

        return '{!s} Lot {!s}'.format(self.contract_notice, self.lot_no)
