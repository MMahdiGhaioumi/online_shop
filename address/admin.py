from django.contrib import admin
from account.admin import my_admin_site
from . import models


class AddressAdmin(admin.ModelAdmin):
    list_select_related = ('city', 'province', 'user')
    list_display = ('body', 'user', 'province', 'city')
    search_fields = ('body', 'city__name', 'province__name', 'user__phone_number')
    sortable_by = ('city', 'province', 'user')
    autocomplete_fields = ('city', 'province', 'user')


class ProvinceAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
    search_fields = ('name',)
    list_filter = ('province',)
    list_select_related = ('province',)
    autocomplete_fields = ('province',)


my_admin_site.register(models.Address, AddressAdmin)
my_admin_site.register(models.Province, ProvinceAdmin)
my_admin_site.register(models.City, CityAdmin)
