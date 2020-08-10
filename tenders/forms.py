'''
Forms for the `tenders` Django app
'''


import os

from django import forms
from django.conf import settings

from tasks.helpers import check_daily_package_exists
from tasks.models import DailyPackageDownloadStatus
from tenders import models, helpers


class UploadXmlFileForm(forms.Form):
    '''
    Form provides fields for a user to upload a single TED export xml file.

    If the data is valid, useful data contained within the file is saved to new entries based on
    the xml file document type:
     * If doc type is contract notice, save as `ContractNotice` and new `Lots`
     * If doc type is contract award notice, save as `ContractAwardNotice` and update existing
       `Lots`
    '''

    upload_file = forms.FileField(required=True, max_length=50, widget=forms.ClearableFileInput())

    def __del__(self):
        '''
        Custom destructor to delete the temporary file if it exists
        '''

        helpers.delete_temporary_file(self.upload_file_path)

    def __init__(self, *args, **kwargs):
        '''
        Override default `__init__()` to store any uploaded files to storage for processing later
        '''

        # Default init
        super().__init__(*args, **kwargs)

        self.n_s = None
        self.root = None
        self.upload_file_path = self.save_temporary_file()

    def clean_upload_file(self):
        '''
        Override field clean to check the uploaded file using `check_xml_file`
        '''

        self.root, self.n_s = helpers.get_xml_root(self.upload_file_path)

        if self.root is not None and self.n_s is not None:
            is_valid, error_strs = helpers.check_xml(self.root, self.n_s)

            # If file is not valid, raise the errors
            if not is_valid:
                for error_str in error_strs:
                    self.upload_file_field_error(error_str)

        else:
            # If `self.root` is `None`, raise error
            self.upload_file_field_error(
                '"' + os.path.basename(self.upload_file_path) + '" file contains invalid syntax.'
            )

        return self.cleaned_data.get('upload_file')

    def save(self):
        '''
        Method saves data contained within `self.root` to new database entries

         * If doc type is contract notice, save as `ContractNotice` and new `Lots`
         * If doc type is contract award notice, save as `ContractAwardNotice` and update existing
           `Lots`
        '''

        new_entry = helpers.create_new_tender(self.root, self.n_s)

        return new_entry

    def save_temporary_file(self):
        '''
        Method saves `upload_file` to a temporary location if it exists, and returns the full path
        of the new temporary file. If `upload_file` is not valid, returns None
        '''

        # Return None by default.
        upload_file_path = None

        upload_file = self.files.get('upload_file', None)

        # if uploaded file exists, save to temp location
        if upload_file:
            upload_file_path = os.path.join(settings.TEMP_FILES_DIR, upload_file.name)

            with open(upload_file_path, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)

        return upload_file_path

    def upload_file_field_error(self, error_str):
        '''
        Create error attached to the `upload_file` field with `error_str`
        '''

        return self.add_error('upload_file', error_str)


class DailyPackageDownloadForm(forms.Form):
    '''
    Form provides a datepicker to allow the user to choose a daily package file to download from
    the TED ftp server
    '''

    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(
            attrs={'data-provide': 'datepicker', 'data-date-format': 'dd/mm/yyyy'}
        )
    )

    def __init__(self, *args, **kwargs):
        '''
        Override default `__init__()` to add attributes
        '''

        # Default init
        super().__init__(*args, **kwargs)

        self.file_name = None

    def clean_date(self):
        '''
        Override field clean to check the date picked by the user

         * If a daily package file for the date has already been downloaded, raise error
         * If a daily package file for the date doesn't exist on the ftp server, raise error
        '''

        date = self.cleaned_data.get('date')

        if DailyPackageDownloadStatus.objects.filter(
            file_date=date, status=DailyPackageDownloadStatus.COMPLETE).exists():
            self.add_error('date', 'Daily package for this date has already been downloaded.')

        else:
            # Check a file exists on the ftp for the given date
            self.file_name = check_daily_package_exists(date)

            # If check returns None, raise error
            if not self.file_name:
                self.add_error(
                    'date', 'Daily package for this date is not available on the ftp server.'
                )

        return date


def contract_notice_file_form(*args, **kwargs):
    '''
    Build a form for the `contract_notice_file` field for `ContractNotice` entries
    '''

    Form = forms.modelform_factory(models.ContractNotice, fields=('procurement_docs_file', ))

    return Form(*args, **kwargs)


def number_of_units_formset(*args, **kwargs):
    '''
    Build a formset for `lots` so we can render an editbox for the `number_of_units` field
    '''

    FormSet = forms.modelformset_factory(models.Lot, fields=('number_of_units', ), extra=0)

    return FormSet(*args, **kwargs)
