from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from . import validators
from . import models


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        max_length=255, label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=validators.password_validators,
        help_text=format_html(
            'رمز عبور باید شرایط زیر را داشته باشد:<br>'
            '• حداقل ۸ و حداکثر ۲۵۵ کاراکتر<br>'
            '• فقط شامل کاراکترهای ASCII<br>'
            '• بدون فاصله یا سایر کاراکترهای فضای خالی<br>'
            '• حداقل یک حرف بزرگ انگلیسی (A-Z)<br>'
            '• حداقل یک حرف کوچک انگلیسی (a-z)<br>'
            '• حداقل یک عدد (0-9)'
        ),
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور', max_length=255,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='باید مانند رمز قبلی باشد.'
    )

    class Meta:
        model = models.User
        fields = ('phone_number', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')
        widgets = {
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
            raise ValidationError("رمزهای عبور یکسان نیستند.", code="password_mismatch")
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
