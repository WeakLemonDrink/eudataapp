'''
Generating views for `profiles` Django web app.
'''


import datetime

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import resolve, reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from profiles import filters, models, tables
from profiles.helpers import get_search_term_matches
from tenders.models import ContractNotice


@login_required
def dashboard(request):
    '''
    Defines the dashboard view for the `profiles` web application
    '''

    query_dict = request.GET.copy()

    # If a `publication_date` querystring hasn't been sent via the request, add one for default
    # filtering by 14 days
    if not query_dict.get('publication_date', None):
        query_dict.update({'publication_date': '14'})

    cn_filter = filters.DashboardPublicationDateFilter(
        query_dict, queryset=ContractNotice.objects.all()
    )


    # First check if user has any search terms at all
    search_term_qs = models.TedSearchTerm.objects.filter(user=request.user, is_active=True)

    # Search for any matches
    search_term_matches = get_search_term_matches(search_term_qs, cn_filter.qs)

    pub_date_duration = query_dict.get('publication_date', None)

    # If the `publication_date` querystring parameter is a date, convert to a datetime obj to pass
    # to context
    try:
        pub_date_duration_dt = datetime.datetime.strptime(pub_date_duration, '%d/%m/%Y')
        pub_date_duration = None

    except ValueError:
        pub_date_duration_dt = None

    # Build the context
    context = {
        'contract_notice_qs': cn_filter.qs,
        'search_term_matches': search_term_matches,
        'pub_date_duration': pub_date_duration,
        'pub_date_duration_dt': pub_date_duration_dt,
        'search_term_qs': search_term_qs
    }

    return render(request, 'profiles/dashboard.html', context)


@login_required
def index(request):
    '''
    Defines the index view for the `profiles` web application
    '''

    # Build the context
    context = {
        'app': apps.get_app_config(resolve(request.path).namespace),
    }

    return render(request, 'profiles/index.html', context)


@login_required
def ted_search_term_update(request, pk):
    '''
    View to update a boolean field to it's opposite value
    '''

    # Get status querystring if it exists
    update_field = request.GET.get('field', None)

    if update_field and update_field in ['send_notifications', 'is_active']:
        # Grab entry and change status if applicable
        entry = get_object_or_404(models.TedSearchTerm.objects.filter(id=pk))

        # Get the current value of the field and set it to the opposite value
        new_value = not getattr(entry, update_field)

        setattr(entry, update_field, new_value)

        entry.save()

        messages.success(
            request,
            str(entry) + ' "' + update_field + '" field updated to "' + str(new_value) + '".'
        )

    else:

        messages.error(request, '"' + str(update_field) + '" field not recognised.')

    # Redirect to the list view
    return HttpResponseRedirect(reverse('profiles:tedsearchterm-list'))


class TedSearchTermCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''
    Defines the create view for new `TedSearchTerm` entries
    '''

    model = models.TedSearchTerm
    fields = ['keyword', 'send_notifications']
    success_message = 'New "%(keyword)s" search term was created successfully.'
    success_url = reverse_lazy('profiles:tedsearchterm-list')

    def form_valid(self, form):
        '''
        Override `form_valid` method to add `request.user` to the `user` ForeignKey for new
        `TedSearchTerm` entries
        '''

        # Add the user to the form
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        '''
        Override default `get_context_data` method to add `model_name` to context via `kwargs`
        '''

        context = super().get_context_data(**kwargs)

        context['app'] = apps.get_app_config(resolve(self.request.path).namespace)
        context['model_name'] = self.model._meta.verbose_name

        return context

    def get_success_url(self):
        '''
        Override `post` method to redirect to `profiles:tedsearchterm-create` instead of default
        `success_url` if the user clicks `Save and add another`
        '''

        if '_addanother' in self.request.POST:
            return self.request.path_info

        # else return the default `success_url`
        return super().get_success_url()


class TedSearchTermDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''
    Defines the delete view for `TedSearchTerm` entries
    '''

    model = models.TedSearchTerm
    success_message = '"%(keyword)s" was deleted successfully.'
    success_url = reverse_lazy('profiles:tedsearchterm-list')

    def delete(self, request, *args, **kwargs):
        '''
        Override default `delete` method to add a success message if the entry is deleted
        '''

        obj = self.get_object()

        # Do this first so we don't return a success message if delete fails
        super_return = super().delete(request, *args, **kwargs)

        messages.success(self.request, self.success_message % obj.__dict__)

        return super_return

    def get_context_data(self, **kwargs):
        '''
        Override default `get_context_data` method to add `model_name` to context via `kwargs`
        '''

        context = super().get_context_data(**kwargs)

        context['app'] = apps.get_app_config(resolve(self.request.path).namespace)
        context['model_name'] = self.model._meta.verbose_name

        return context


class TedSearchTermListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    '''
    Defines the list view for `TedSearchTerm` entries
    '''

    model = models.TedSearchTerm
    filterset_class = filters.TedSearchTermFilter
    table_class = tables.TedSearchTermTable
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        '''
        Override default `get_context_data` method to add `model_name` to context via `kwargs`
        '''

        context = super().get_context_data(**kwargs)

        context['app'] = apps.get_app_config(resolve(self.request.path).namespace)
        context['model_name'] = self.model._meta.verbose_name

        return context

    def get_queryset(self):
        '''
        Override default `get_queryset` method to filter returned `TedSearchTerm` entries by
        `request.user`
        '''

        return self.model.objects.filter(user=self.request.user)
