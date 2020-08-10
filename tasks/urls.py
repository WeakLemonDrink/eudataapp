'''
Mapping urls for `tasks` Django web app.
'''


from django.urls import path

from tasks import views


app_name = 'tasks'
urlpatterns = [
    path('bulk-upload-progress/<str:file_name>/', views.bulk_upload_progress,
         name='bulk-upload-progress'),
    path('get-task-status/<str:file_name>/', views.get_task_status, name='get-task-status')
]
