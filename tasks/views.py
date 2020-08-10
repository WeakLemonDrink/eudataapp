'''
Generating views for `tasks` Django web app.
'''


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from tasks.models import DailyPackageDownloadStatus


@csrf_protect
@login_required
def bulk_upload_progress(request, file_name):
    '''
    Returns `DailyPackageDownloadStatus` entry which stores the progress of
    `tasks.bulk_tender_create_task`

    If status is COMPLETE or ERROR, redirect to the `tenders:list` page with associated msg
    '''

    status_entry = get_object_or_404(DailyPackageDownloadStatus, file_name=file_name)

    status = status_entry.status

    if status in [DailyPackageDownloadStatus.COMPLETE, DailyPackageDownloadStatus.ERROR]:

        if status == DailyPackageDownloadStatus.COMPLETE:
            message_tag = messages.SUCCESS
        else:
            message_tag = messages.ERROR

        messages.add_message(request, message_tag, status_entry.status_msg)

        response = HttpResponseRedirect(reverse('tenders:contractnotice-list'))

    else:
        response = render(request, 'tasks/bulk_upload_progress.html', {'status': status_entry})

    return response


@csrf_protect
@login_required
def get_task_status(request, file_name):
    '''
    Returns json of status contained within `DailyPackageDownloadStatus` to show progress of
    `tasks.bulk_tender_create_task`
    '''

    status = get_object_or_404(DailyPackageDownloadStatus, file_name=file_name)

    context = {
        'file_name': status.file_name,
        'status': status.status,
        'status_msg': status.status_msg,
        'get_status_display': status.get_status_display()
    }

    return JsonResponse(context)
