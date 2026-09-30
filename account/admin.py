from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from . import models
from . import forms


class MyAdminSite(admin.AdminSite):
    site_header = 'فروشگاه اینترنتی'
    site_title = 'صفحه مدیریت فروشگاه'
    index_title = 'صفحه مدیریت فروشگاه'


my_admin_site = MyAdminSite('my_admin')


class UserAdmin(BaseUserAdmin):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    list_display = ('phone_number', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('is_active', 'role', 'is_superuser', 'is_staff')
    search_fields = ('phone_number', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    empty_value_display = "-empty-"
    readonly_fields = ('date_joined', 'last_login')
    sortable_by = ('role', 'is_active', 'first_name', 'last_name')

    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['password1', 'password2', 'phone_number', ('first_name', 'last_name'), 'role', 'is_staff',
                       'is_superuser'],
        })
    ]

    fieldsets = [
        ('حساب کاربری', {
            'classes': ['wide'],
            'fields': [
                'phone_number',
                'password',
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
            ]
        }),
        ('اطلاعات کاربر', {
            'classes': ['collapse'],
            'fields': [
                ('first_name', 'last_name'),
                'birth_date',
                'date_joined',
                'last_login',
                'image',
            ]
        }),
        ('گروه‌ها و دسترسی‌ها', {
            'classes': ['collapse'],
            'fields': [
                'groups',
                'user_permissions',
            ]
        })
    ]


my_admin_site.register(models.User, UserAdmin)
my_admin_site.register(Group)