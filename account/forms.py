from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from . import models

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        max_length=255, label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور', max_length=255,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = models.User
        fields = ('phone_number', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = '__all__'