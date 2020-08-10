'''
Generating views for `tenders` Django web app.
'''


import os

from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import resolve, reverse, reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import ContextMixin, View

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from tasks import tasks
from tasks.models import DailyPackageDownloadStatus
from tenders import filters, forms, helpers, models, tables


@login_required
def index(request):
    '''
    Defines the index view for the `tenders` web application
    '''

    # Build the context
    context = {
        'app': apps.get_app_config(resolve(request.path).namespace),
        'total_contract_award_notice': models.ContractAwardNotice.objects.all().count(),
        'total_contract_notice': models.ContractNotice.objects.all().count(),
        'total_lots': models.Lot.objects.all().count(),
    }

    # Get the latest `DailyPackageDownloadStatus` entry if it exists
    if DailyPackageDownloadStatus.objects.exists():
        context['latest_status'] = DailyPackageDownloadStatus.objects.all().latest('added')

    return render(request, 'tenders/index.html', context)


@csrf_protect
@login_required
def sign_s3(request):
    '''
    Returns a signed url for file upload to S3 using credentials from S3 Client
    '''

    bucket = settings.AWS_STORAGE_BUCKET_NAME

    file_key = os.path.join(settings.TMP_LOCATION, request.GET['file_name'])
    file_type = request.GET['file_type']

    s3_client = helpers.new_s3_client()

    presigned_post = s3_client.generate_presigned_post(
        Bucket=bucket,
        Key=file_key,
        Fields={'Content-Type': file_type},
        Conditions=[{'Content-Type': file_type}],
        ExpiresIn=3600
    )

    return JsonResponse({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (bucket, file_key)
    })


class ContractNoticeListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    '''
    Defines the list view for `ContractNotice` entries
    '''

    model = models.ContractNotice
    filterset_class = filters.ContractNoticeFilter
    table_class = tables.ContractNoticeTable
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        '''
        Override default `get_context_data` method to add `model_name` to context via `kwargs`
        '''

        context = super().get_context_data(**kwargs)

        context['app'] = apps.get_app_config(resolve(self.request.path).namespace)
        context['model_name'] = self.model._meta.verbose_name

        return context

    def get_filterset_kwargs(self, filterset_class):
        '''
        Override default `get_filterset_kwargs` to add `user` kwarg so we can construct filter
        based on user
        '''

        kwargs = super().get_filterset_kwargs(filterset_class)

        # Add `user` to the kwargs
        kwargs.update({'user': self.request.user})

        return kwargs


class LotListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    '''
    Defines the list view for `Lot` entries
    '''

    model = models.Lot
    filterset_class = filters.LotFilter
    queryset = models.Lot.objects.all()
    table_class = tables.LotTable
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        '''
        Override default `get_context_data` method to add `model_name` to context via `kwargs`
        '''

        context = super().get_context_data(**kwargs)

        context['app'] = apps.get_app_config(resolve(self.request.path).namespace)
        context['model_name'] = self.model._meta.verbose_name

        return context


class ContractNoticeEditLotUnitsView(LoginRequiredMixin, ContextMixin, View):
    '''
    Defines a view to edit `number_of_units` data per `Lot` for a `ContractNotice` entry
    '''

    template_name = 'tenders/contractnotice_edit_lot_units.html'

    def get(self, request, *args, **kwargs):
        '''
        Renders the new form so user can upload data when get request
        '''

        contract_notice = get_object_or_404(
            models.ContractNotice.objects.filter(id=kwargs.get('contractnotice_id'))
        )

        # Build context ready to pass to render
        context = self.get_context_data(
            lot_formset=forms.number_of_units_formset(queryset=contract_notice.lot_set.all()),
            contract_notice=contract_notice,
            contract_notice_form=forms.contract_notice_file_form(instance=contract_notice)
        )

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        '''
        Handles post data and returns created `tender` data when successful
        '''

        contract_notice = get_object_or_404(
            models.ContractNotice.objects.filter(id=kwargs.get('contractnotice_id'))
        )

        lot_formset = forms.number_of_units_formset(request.POST, request.FILES,
                                                    queryset=contract_notice.lot_set.all())
        contract_notice_form = forms.contract_notice_file_form(request.POST, request.FILES,
                                                               instance=contract_notice)

        # If data entered is valid, save the data
        if lot_formset.is_valid() and contract_notice_form.is_valid():

            lot_formset.save()
            contract_notice_form.save()

            messages.success(
                request,
                'ContractNotice ' + str(contract_notice) + ' and associated lots updated ' + \
                'successfully.'
            )

            # Redirect to a view that shows progress
            response = HttpResponseRedirect(reverse_lazy('tenders:contractnotice-list'))

        else:
            # If not valid, return the form with associated errors
            # Build context ready to pass to render
            context = self.get_context_data(
                contract_notice=contract_notice, contract_notice_form=contract_notice_form,
                lot_formset=lot_formset
            )

            response = render(request, self.template_name, context)

        return response


class TenderBulkCreateView(LoginRequiredMixin, ContextMixin, View):
    '''
    Defines the create view for multiple `Tender` entries
    '''

    form_class = forms.DailyPackageDownloadForm
    template_name = 'tenders/tender_bulk_create.html'

    def get(self, request, *args, **kwargs):
        '''
        Renders the new form so user can upload data when get request
        '''

        # Build context ready to pass to render
        context = self.get_context_data(form=self.form_class())

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        '''
        Override default `get_context_data` method to add `upload_file_desc` to context via
        `kwargs`
        '''

        context = super().get_context_data(**kwargs)

        context['upload_file_desc'] = 'TED daily download archive file'

        return context

    def post(self, request, *args, **kwargs):
        '''
        Handles post data and returns created `tender` data when successful
        '''

        form = self.form_class(request.POST)

        # If data entered is valid, fire off the task to check the file and create new
        # `ContractAwardNotice`, `ContractNotice` and `Lot` entries
        if form.is_valid():

            # Create a new `DailyPackageDownloadStatus` entry to track processing progress
            DailyPackageDownloadStatus.objects.get_or_create(file_name=form.file_name)

            tasks.bulk_tender_create_task.delay(form.file_name)

            # Redirect to a view that shows progress
            response = HttpResponseRedirect(
                reverse('tasks:bulk-upload-progress', args=[form.file_name])
            )

        else:
            # If not valid, return the form with associated errors
            # Build context ready to pass to render
            context = self.get_context_data(form=form)

            response = render(request, self.template_name, context)

        return response


class TenderSingleCreateView(LoginRequiredMixin, ContextMixin, View):
    '''
    Defines the create view for a single `ContractNotice` or `ContractAwardNotice` entry
    '''

    form_class = forms.UploadXmlFileForm
    template_name = 'tenders/tender_single_create.html'

    def get(self, request, *args, **kwargs):
        '''
        Renders the new form so user can upload data when get request
        '''

        # Build context ready to pass to render
        context = self.get_context_data(form=self.form_class())

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        '''
        Override default `get_context_data` method to add `upload_file_desc` to context via
        `kwargs`
        '''

        context = super().get_context_data(**kwargs)

        context['upload_file_desc'] = 'single TED export xml file'

        return context

    def post(self, request, *args, **kwargs):
        '''
        Handles post data and returns a created `ContractNotice` or `ContractAwardNotice` data
        when successful
        '''

        form = self.form_class(request.POST, request.FILES)

        # If data entered is valid, call `form.save()` to create new entries
        if form.is_valid():

            new_entry = form.save()

            # Create the success message
            messages.add_message(
                request,
                messages.SUCCESS,
                '{} {} was added to the database successfully.'.format(
                    new_entry._meta.verbose_name, new_entry
                )
            )

            # Redirect to a view showing success
            response = HttpResponseRedirect(
                reverse('tenders:{}-list'.format(new_entry._meta.model_name))
            )

        else:
            # If not valid, return the form with associated errors
            # Build context ready to pass to render
            context = self.get_context_data(form=form)

            response = render(request, self.template_name, context)

        return response


class ContractAwardNoticeListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    '''
    Defines the list view for `ContractAwardNotice` entries
    '''

    model = models.ContractAwardNotice
    filterset_class = filters.ContractAwardNoticeFilter
    table_class = tables.ContractAwardNoticeTable
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        '''
        Override default `get_context_data` method to add `model_name` to context via `kwargs`
        '''

        context = super().get_context_data(**kwargs)

        context['app'] = apps.get_app_config(resolve(self.request.path).namespace)
        context['model_name'] = self.model._meta.verbose_name

        return context
