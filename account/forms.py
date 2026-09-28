from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
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

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password2 != password1:
            raise ValidationError("Passwords don't match", code="password_mismatch")
        return password2

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))

        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = '__all__'
