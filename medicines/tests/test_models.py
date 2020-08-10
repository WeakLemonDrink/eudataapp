'''
Tests for `medicines.models` in the `medicines` Django web application
'''


from django.test import TestCase

from medicines import models


class BNFChemicalSubstanceModelTests(TestCase):
    '''
    TestCase class for the `BNFChemicalSubstance` model
    '''

    def test_str_method_return_string(self):
        '''
        `BNFChemicalSubstance` model entry `__str__()` method should return the `name`

        e.g. 'Tramadol Hydrochloride'
        '''

        entry = models.BNFChemicalSubstance.objects.create(
            code='040702040', name='Tramadol Hydrochloride'
        )

        self.assertEqual(str(entry), 'Tramadol Hydrochloride')


class BNFProductModelTests(TestCase):
    '''
    TestCase class for the `BNFProduct` model
    '''

    def test_str_method_return_string(self):
        '''
        `BNFProduct` model entry `__str__()` method should return the `name`

        e.g. 'Tramadol HCl'
        '''

        entry = models.BNFProduct.objects.create(
            code='040702040AA', name='Tramadol HCl'
        )

        self.assertEqual(str(entry), 'Tramadol HCl')

    def test_save_is_generic_true_if_code_endswith_aa(self):
        '''
        `BNFProduct` model entry `save()` method should set `is_generic` field to `True` if `code`
        endwith `AA`

        `AA` product code shows that the product is generic
        '''

        entry = models.BNFProduct.objects.create(
            code='040702040AA', name='Tramadol HCl'
        )

        self.assertTrue(entry.is_generic)

    def test_save_is_generic_false_if_code_not_endswith_aa(self):
        '''
        `BNFProduct` model entry `save()` method should not set `is_generic` field to `True` if
        `code` doesn't endwith `AA`

        A product code other than `AA` shows that the product is not generic. `save()` method
        should not update `is_generic` field which is set to `False` by default
        '''

        entry = models.BNFProduct.objects.create(
            code='0407010X0CD', name='Boots (Paracet Combined)'
        )

        self.assertFalse(entry.is_generic)


class BNFPresentationModelTests(TestCase):
    '''
    TestCase class for the `BNFPresentation` model
    '''

    def setUp(self):
        '''
        common setup
        '''

        chemical_substance = models.BNFChemicalSubstance.objects.create(
            code='0407010X0', name='Paracetamol Combined Preparations'
        )
        product = models.BNFProduct.objects.create(
            code='0407010X0CD', name='Boots (Paracet Combined)'
        )

        self.entry = models.BNFPresentation.objects.create(
            chem_substance=chemical_substance, product=product,
            code='0407010X0CDAFA0', name='Boots_Pharmacy Cold & Flu Day Cap')

    def test_str_method_return_string(self):
        '''
        `BNFPresentation` model entry `__str__()` method should return the `code` and `title`

        e.g. 'Boots_Pharmacy Cold & Flu Day Cap'
        '''

        self.assertEqual(str(self.entry), 'Boots_Pharmacy Cold & Flu Day Cap')

    def test_get_absolute_url_returns_url(self):
        '''
        `BNFPresentation` model entry `get_absolute_url()` method should return a url using the
        `code` as the id
        '''

        expected_url = '/medicines/bnf-presentation/' + self.entry.code + '/'

        self.assertEqual(expected_url, self.entry.get_absolute_url())
