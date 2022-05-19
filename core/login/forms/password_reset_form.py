from django import forms

from core.login.models import User


class PasswordResetForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese su nombre de usuario',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()

        if not User.objects.filter(username=cleaned_data['username']).exists():
            raise forms.ValidationError("El usuario no existe")

        return cleaned_data

    def get_user(self):
        if self.user:
            return self.user

        username = self.cleaned_data['username']

        self.user = User.objects.get(username=username)

        return self.get_user()
