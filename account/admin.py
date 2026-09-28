from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
from . import forms


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    list_display = ('__str__', 'first_name',  'role', 'is_active')
    list_filter = ()
    search_fields = ()
    empty_value_display = "-empty-"

    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['password1', 'password2', 'phone_number', ('first_name', 'last_name'), 'role', 'is_staff', 'is_superuser'],
        })
    ]

    fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['phone_number', ('first_name', 'last_name'), 'role', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'birth_date', 'groups', 'image', 'last_login', 'user_permissions', 'password']
        })
    ]
    ordering = ()