'''
Models for the `medicines` Django app
'''


from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.urls import reverse


class BNFChemicalSubstance(models.Model):
    '''
    Defines database table structure for `BNFChemicalSubstance` entries

    British National Formulary (BNF) Chemical Substances
    '''

    code = models.CharField('Code', max_length=10)
    name = models.CharField('Name', max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'medicines'
        ordering = ['code']
        verbose_name = 'BNF Chemical Substance'

    def __str__(self):
        '''
        Defines the return string for a `BNFChemicalSubstance` entry
        '''

        return self.name


class BNFProduct(models.Model):
    '''
    Defines database table structure for `BNFProduct` entries

    British National Formulary (BNF) Products
    '''

    code = models.CharField('Code', max_length=12)
    name = models.CharField('Name', max_length=140)
    is_active = models.BooleanField(default=True)
    is_generic = models.BooleanField(default=False)

    class Meta:
        app_label = 'medicines'
        ordering = ['code']
        verbose_name = 'BNF Product'

    def save(self, *args, **kwargs):
        '''
        Override default save to set `is_generic = True` if generic code is used

        "AA" at the end of `self.code` shows the product is generic
        '''

        # Only do on initial save
        if self.pk is None:
            if self.code.endswith('AA'):
                self.is_generic = True

        # Call default save
        super().save(*args, **kwargs)

    def __str__(self):
        '''
        Defines the return string for a `BNFProduct` entry
        '''

        return self.name


class BNFPresentation(models.Model):
    '''
    Defines database table structure for `BNFPresentation` entries

    `BNFPresentation` entries are in the format of the British National Formulary (BNF). Fields are
    taken from the BNF download available from
    https://apps.nhsbsa.nhs.uk/infosystems/data/showDataSelector.do?reportId=126
    '''

    chem_substance = models.ForeignKey(BNFChemicalSubstance, on_delete=models.CASCADE,
                                       verbose_name='BNF Chemical Substance')
    product = models.ForeignKey(BNFProduct, on_delete=models.CASCADE, verbose_name='BNF Product')
    code = models.CharField('Code', max_length=20)
    name = models.CharField('Name', max_length=140)
    is_active = models.BooleanField(default=True)
    search_vector = SearchVectorField(null=True, editable=False)

    def get_absolute_url(self):
        '''
        Method returns the specific url of a `BNFPresentation` entry
        '''

        return reverse('medicines:bnfpresentation-detail', args=(self.code, ))


    class Meta:
        app_label = 'medicines'
        ordering = ['code']
        verbose_name = 'BNF Presentation'

    def __str__(self):
        '''
        Defines the return string for a `BNFPresentation` entry
        '''

        return self.name
