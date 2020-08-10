'''
Admin config for `tasks` Django web app
'''


from django.contrib import admin

from tasks import models


class DailyPackageDownloadStatusAdmin(admin.ModelAdmin):
    '''
    Custom `DailyPackageDownloadStatus` class defines admin display
    '''

    list_display = ('file_name', 'file_date', 'added', 'modified', 'status', 'status_msg')

    def has_add_permission(self, request):
        '''
        Override disables add option in the admin
        '''

        return False

    def has_change_permission(self, request, obj=None):
        '''
        Override disables change/edit option in the admin
        '''

        return False


class EmailNotificationStatusAdmin(admin.ModelAdmin):
    '''
    Custom `EmailNotificationStatus` class defines admin display
    '''

    list_display = ('user', 'publication_date', 'added', 'modified', 'status', 'status_msg')

    def has_add_permission(self, request):
        '''
        Override disables add option in the admin
        '''

        return False

    def has_change_permission(self, request, obj=None):
        '''
        Override disables change/edit option in the admin
        '''

        return False


admin.site.register(models.DailyPackageDownloadStatus, DailyPackageDownloadStatusAdmin)
admin.site.register(models.EmailNotificationStatus, EmailNotificationStatusAdmin)
