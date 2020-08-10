'''
Generating views for `medicines` Django web app.
'''


import requests

from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import resolve
from django.views.generic.detail import DetailView

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from medicines import filters, models, tables
from medicines.helpers import process_pricing_data


@login_required
def index(request):
    '''
    Defines the index view for the `medicines` web application
    '''

    # Build the context
    context = {
        'app': apps.get_app_config(resolve(request.path).namespace),
        'total_chem_substance': models.BNFChemicalSubstance.objects.all().count(),
        'total_presentation': models.BNFPresentation.objects.all().count(),
        'total_product': models.BNFProduct.objects.all().count(),
    }

    return render(request, 'medicines/index.html', context)


def get_pricing_data(request, code):
    '''
    Queries the OpenPrescribing api and retrieves pricing data for the input `code`

    OpenPrescribing returns a list of dictionaries containing:
      {"items":32961,"quantity":1114647,"actual_cost":956153.35,"date":"2014-11-01"}

    price_per_unit = actual_cost / quantity

    Data is processed to calculate price_per_unit and returns a JsonResponse of a list of
    dictionaries containing:
      {"price_per_unit":0.8578082119271841,"date":"2014-11-01"}
    '''

    # Query the Open Prescribing API and get the json response
    response = requests.get(
        settings.OPEN_PRESCRIBING_API_URL + '?code=' + code + '&format=json'
    )

    # Process the data to calculate price_per_unit. price_per_unit = actual_cost / quantity
    processed_data = process_pricing_data(response.json())

    return JsonResponse(processed_data, safe=False)


class BNFPresentationListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    '''
    Defines the list view for `BNFPresentation` entries
    '''

    model = models.BNFPresentation
    filterset_class = filters.BNFPresentationFilter
    queryset = models.BNFPresentation.objects.all()
    table_class = tables.BNFPresentationTable
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        '''
        Override default `get_context_data` method to add `model_name` to context via `kwargs`
        '''

        context = super().get_context_data(**kwargs)

        context['app'] = apps.get_app_config(resolve(self.request.path).namespace)
        context['model_name'] = self.model._meta.verbose_name

        return context


class BNFPresentationDetailView(LoginRequiredMixin, DetailView):
    '''
    Defines the detail view for `BNFPresentation` entries
    '''

    model = models.BNFPresentation
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_context_data(self, **kwargs):
        '''
        Override default `get_context_data` method to add `model_name` to context via `kwargs`
        '''

        context = super().get_context_data(**kwargs)

        context['app'] = apps.get_app_config(resolve(self.request.path).namespace)
        context['model_name'] = self.model._meta.verbose_name

        return context
