from django import forms
from django.contrib.auth import password_validation

from core.login.models import User


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese su nueva contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita su nueva contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token')
        self.user = User.objects.get(token=self.token)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas deben ser iguales")

        password_validation.validate_password(password1, self.get_user())

        return cleaned_data

    def get_user(self):
        if self.user:
            return self.user

        self.user = User.objects.get(token=self.token)

        return self.get_user()
