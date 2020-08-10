'''
Admin config for `tenders` Django web app
'''


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User

from tenders import models


class CommonAdmin(admin.ModelAdmin):
    '''
    Common admin class to inherit across the different models
    '''

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

    def has_delete_permission(self, request, obj=None):
        '''
        Override disables delete option in the admin
        '''

        return False


class CountryAdmin(CommonAdmin):
    '''
    Custom `Country` class defines admin display
    '''

    list_display = ('iso_code', 'country_name', 'is_active')


class CurrencyAdmin(CommonAdmin):
    '''
    Custom `Currency` class defines admin display
    '''

    list_display = ('iso_code', 'currency_name', 'is_active')


class UserAdmin(BaseUserAdmin):
    '''
    Custom `User` class defines admin display
    '''

    list_display = ('username', 'first_name', 'last_name', 'last_login', 'is_staff', 'is_active')


admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(User, UserAdmin)

admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.Currency, CurrencyAdmin)
